from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext
import secrets
import pyotp
import qrcode
import io
import base64
import json

from app.database_alchemy.models.user import User
from app.database_alchemy.models.tenant import Tenant
# Import OTP model - will be available after migration
# from app.database.models.user.otp import Otp
from app.database_alchemy.models.auth_token import AuthToken
from app.database_alchemy.models.user_external_auth import UserExternalAuth
from app.auth.jwt_service import JWTService
from app.config.config import get_settings
from app.domain_types.miscellaneous.exceptions import NotFound, Conflict
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

# Initialize password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_or_create_tenant(session: Session, tenant_code: str = None) -> Tenant:
        """Get or create tenant"""
        if not tenant_code:
            tenant_code = settings.DEFAULT_TENANT_ID

        tenant = session.query(Tenant).filter(Tenant.Code == tenant_code).first()
        if not tenant:
            # Create default tenant if it doesn't exist
            tenant = Tenant(
                Name="Default Tenant" if tenant_code == settings.DEFAULT_TENANT_ID else tenant_code.title(),
                Code=tenant_code,
                IsDefault=(tenant_code == settings.DEFAULT_TENANT_ID),
                IsActive=True
            )
            session.add(tenant)
            session.commit()
            session.refresh(tenant)

        return tenant

    @staticmethod
    def authenticate_with_email_password(
        session: Session,
        email: str,
        password: str,
        tenant_id: str = None
    ) -> Tuple[Optional[User], Optional[str]]:
        """Authenticate user with email and password"""
        if not settings.ENABLE_EMAIL_PASSWORD_AUTH:
            return None, "Email/password authentication is disabled"

        tenant = AuthService.get_or_create_tenant(session, tenant_id)

        user = session.query(User).filter(
            func.lower(User.Email) == func.lower(email),
            User.TenantId == tenant.id,
            User.IsActive == True
        ).first()

        if not user:
            return None, "Invalid email or password"

        if not user.Password:
            return None, "Password not set for this user"

        # Check if user is locked
        if user.LockedUntil and user.LockedUntil > datetime.utcnow():
            return None, f"Account locked until {user.LockedUntil}"

        if not AuthService.verify_password(password, user.Password):
            # Increment failed login attempts
            user.FailedLoginAttempts = (user.FailedLoginAttempts or 0) + 1
            if user.FailedLoginAttempts >= 5:  # Lock after 5 failed attempts
                user.LockedUntil = datetime.utcnow() + timedelta(minutes=30)
            session.commit()
            return None, "Invalid email or password"

        # Reset failed attempts on successful login
        user.FailedLoginAttempts = 0
        user.LockedUntil = None
        user.LastLoginAt = datetime.utcnow()
        session.commit()

        return user, None

    @staticmethod
    def authenticate_with_phone_password(
        session: Session,
        phone: str,
        password: str,
        tenant_id: str = None
    ) -> Tuple[Optional[User], Optional[str]]:
        """Authenticate user with phone and password"""
        if not settings.ENABLE_EMAIL_PASSWORD_AUTH:
            return None, "Phone/password authentication is disabled"

        tenant = AuthService.get_or_create_tenant(session, tenant_id)

        user = session.query(User).filter(
            User.Phone == phone,
            User.TenantId == tenant.id,
            User.IsActive == True
        ).first()

        if not user:
            return None, "Invalid phone or password"

        if not user.Password:
            return None, "Password not set for this user"

        # Check if user is locked
        if user.LockedUntil and user.LockedUntil > datetime.utcnow():
            return None, f"Account locked until {user.LockedUntil}"

        if not AuthService.verify_password(password, user.Password):
            # Increment failed login attempts
            user.FailedLoginAttempts = (user.FailedLoginAttempts or 0) + 1
            if user.FailedLoginAttempts >= 5:
                user.LockedUntil = datetime.utcnow() + timedelta(minutes=30)
            session.commit()
            return None, "Invalid phone or password"

        # Reset failed attempts on successful login
        user.FailedLoginAttempts = 0
        user.LockedUntil = None
        user.LastLoginAt = datetime.utcnow()
        session.commit()

        return user, None

    @staticmethod
    def generate_otp(session: Session, user_id: str, purpose: str, phone: str = None, email: str = None) -> str:
        """Generate OTP for user"""
        if not settings.ENABLE_PHONE_OTP_AUTH:
            raise Exception("OTP authentication is disabled")

        # Invalidate existing OTPs for same purpose
        session.query(Otp).filter(
            Otp.UserId == user_id,
            Otp.Purpose == purpose,
            Otp.IsUsed == False
        ).update({"IsUsed": True})

        # Generate OTP code
        otp_code = ''.join([str(secrets.randbelow(10)) for _ in range(settings.OTP_LENGTH)])

        # Create OTP record
        otp = Otp(
            UserId=user_id,
            Code=otp_code,
            Purpose=purpose,
            PhoneNumber=phone,
            Email=email,
            ExpiresAt=datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
        )
        session.add(otp)
        session.commit()

        return otp_code

    @staticmethod
    def verify_otp(session: Session, user_id: str, otp_code: str, purpose: str) -> bool:
        """Verify OTP code"""
        otp = session.query(Otp).filter(
            Otp.UserId == user_id,
            Otp.Code == otp_code,
            Otp.Purpose == purpose,
            Otp.IsUsed == False,
            Otp.ExpiresAt > datetime.utcnow()
        ).first()

        if not otp:
            return False

        # Increment attempt count
        otp.AttemptCount += 1

        if otp.AttemptCount > settings.OTP_MAX_ATTEMPTS:
            otp.IsUsed = True
            session.commit()
            return False

        # Mark as used
        otp.IsUsed = True
        session.commit()

        return True

    @staticmethod
    def authenticate_with_phone_otp(
        session: Session,
        phone: str,
        otp_code: str,
        tenant_id: str = None
    ) -> Tuple[Optional[User], Optional[str]]:
        """Authenticate user with phone and OTP"""
        if not settings.ENABLE_PHONE_OTP_AUTH:
            return None, "Phone OTP authentication is disabled"

        tenant = AuthService.get_or_create_tenant(session, tenant_id)

        user = session.query(User).filter(
            User.Phone == phone,
            User.TenantId == tenant.id,
            User.IsActive == True
        ).first()

        if not user:
            return None, "Invalid phone number"

        if not AuthService.verify_otp(session, user.id, otp_code, "login"):
            return None, "Invalid or expired OTP"

        user.LastLoginAt = datetime.utcnow()
        session.commit()

        return user, None

    @staticmethod
    def setup_two_factor(session: Session, user_id: str) -> Dict[str, Any]:
        """Setup two-factor authentication for user"""
        if not settings.ENABLE_TWO_FACTOR_AUTH:
            raise Exception("Two-factor authentication is disabled")

        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFound("User not found")

        # Generate TOTP secret
        secret = pyotp.random_base32()

        # Create TOTP URI
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user.Email or user.Phone,
            issuer_name=settings.SERVICE_NAME
        )

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Save secret (temporarily, until verified)
        user.TwoFactorSecret = secret
        session.commit()

        return {
            "secret": secret,
            "qr_code": f"data:image/png;base64,{qr_code_base64}",
            "provisioning_uri": provisioning_uri
        }

    @staticmethod
    def verify_two_factor_setup(session: Session, user_id: str, totp_code: str) -> bool:
        """Verify two-factor setup"""
        user = session.query(User).filter(User.id == user_id).first()
        if not user or not user.TwoFactorSecret:
            return False

        totp = pyotp.TOTP(user.TwoFactorSecret)
        if totp.verify(totp_code):
            user.IsTwoFactorEnabled = True
            session.commit()
            return True

        return False

    @staticmethod
    def verify_two_factor(session: Session, user_id: str, totp_code: str) -> bool:
        """Verify two-factor authentication code"""
        user = session.query(User).filter(User.id == user_id).first()
        if not user or not user.IsTwoFactorEnabled or not user.TwoFactorSecret:
            return False

        totp = pyotp.TOTP(user.TwoFactorSecret)
        return totp.verify(totp_code)

    @staticmethod
    def get_user_roles(user_id: str, session: Session) -> List[str]:
        """Get user roles from database"""
        try:
            from app.database_alchemy.models.user_role import UserRole
            from app.database_alchemy.models.role import Role

            user_roles = session.query(UserRole).join(Role).filter(
                UserRole.UserId == user_id
            ).all()

            return [ur.role.RoleName for ur in user_roles if ur.role]
        except Exception as e:
            # If role tables don't exist yet or there's an error, return empty list
            logger.warning(f"Could not fetch user roles: {str(e)}")
            return []

    @staticmethod
    def create_user_tokens(session: Session, user: User) -> Dict[str, str]:
        """Create access and refresh tokens for user"""
        # Get user roles from database
        roles = AuthService.get_user_roles(user.id, session)

        access_token = JWTService.create_access_token(
            user_id=user.id,
            tenant_id=user.TenantId,
            roles=roles
        )

        refresh_token = JWTService.create_refresh_token(
            user_id=user.id,
            tenant_id=user.TenantId,
            session=session
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    @staticmethod
    def refresh_access_token(session: Session, refresh_token: str) -> Optional[Dict[str, str]]:
        """Refresh access token using refresh token"""
        payload = JWTService.verify_token(refresh_token, "refresh")
        if not payload:
            return None

        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")

        # Check if refresh token is revoked
        if JWTService.is_token_revoked(refresh_token, session):
            return None

        # Get user
        user = session.query(User).filter(
            User.id == user_id,
            User.TenantId == tenant_id,
            User.IsActive == True
        ).first()

        if not user:
            return None

        # Create new tokens
        return AuthService.create_user_tokens(session, user)

    @staticmethod
    def create_external_auth_user(
        session: Session,
        provider: str,
        external_user_id: str,
        email: str,
        display_name: str,
        tenant_id: str = None,
        additional_data: Dict[str, Any] = None
    ) -> User:
        """Create user from external authentication provider"""
        tenant = AuthService.get_or_create_tenant(session, tenant_id)

        # Check if user already exists
        existing_auth = session.query(UserExternalAuth).filter(
            UserExternalAuth.Provider == provider,
            UserExternalAuth.ExternalUserId == external_user_id
        ).first()

        if existing_auth:
            return session.query(User).filter(User.id == existing_auth.UserId).first()

        # Check if user exists with same email in tenant
        existing_user = session.query(User).filter(
            func.lower(User.Email) == func.lower(email),
            User.TenantId == tenant.id
        ).first()

        if existing_user:
            # Link existing user to external provider
            external_auth = UserExternalAuth(
                UserId=existing_user.id,
                Provider=provider,
                ExternalUserId=external_user_id,
                Email=email,
                DisplayName=display_name,
                AdditionalData=json.dumps(additional_data) if additional_data else None
            )
            session.add(external_auth)
            session.commit()
            return existing_user

        # Create new user
        names = display_name.split(" ", 1) if display_name else ["", ""]
        user = User(
            TenantId=tenant.id,
            FirstName=names[0] if len(names) > 0 else None,
            LastName=names[1] if len(names) > 1 else None,
            Email=email,
            IsEmailVerified=True,  # Assume verified from external provider
            IsActive=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create external auth record
        external_auth = UserExternalAuth(
            UserId=user.id,
            Provider=provider,
            ExternalUserId=external_user_id,
            Email=email,
            DisplayName=display_name,
            AdditionalData=json.dumps(additional_data) if additional_data else None
        )
        session.add(external_auth)
        session.commit()

        return user
