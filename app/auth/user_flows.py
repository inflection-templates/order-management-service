from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
import secrets
import logging

from app.database.models.user import User
from app.database.models.tenant import Tenant
from app.database.models.auth_token import AuthToken
# Import OTP model - will be available after migration
# from app.database.models.user.otp import Otp
from app.auth.jwt_service import JWTService
from app.auth.auth_service import AuthService
from app.auth.email_service import EmailService
from app.auth.sms_service import SMSService
from app.config.config import get_settings
from app.domain_types.miscellaneous.exceptions import NotFound, Conflict

logger = logging.getLogger(__name__)
settings = get_settings()

class UserFlowService:

    @staticmethod
    def send_invitation_email(
        session: Session,
        email: str,
        first_name: str = None,
        last_name: str = None,
        role_ids: list = None,
        tenant_id: str = None,
        message: str = None,
        invited_by_user_id: str = None
    ) -> str:
        """Send invitation email to user"""
        tenant = AuthService.get_or_create_tenant(session, tenant_id)

        # Check if user already exists
        existing_user = session.query(User).filter(
            func.lower(User.Email) == func.lower(email),
            User.TenantId == tenant.id
        ).first()

        if existing_user:
            raise Conflict("User already exists in this tenant")

        # Create inactive user record
        user = User(
            TenantId=tenant.id,
            FirstName=first_name,
            LastName=last_name,
            Email=email,
            IsActive=False,  # Will be activated when invitation is accepted
            IsEmailVerified=False
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create invitation token
        invitation_token = JWTService.create_special_token(
            user_id=user.id,
            tenant_id=tenant.id,
            token_type="invitation",
            session=session,
            expires_hours=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS,
            additional_claims={
                "email": email,
                "role_ids": role_ids or [],
                "invited_by": invited_by_user_id,
                "message": message
            }
        )

        # Send actual invitation email
        invitation_link = f"{settings.BASE_URL}/auth/accept-invitation?token={invitation_token}"
        inviter_name = None
        if invited_by_user_id:
            inviter = session.query(User).filter(User.id == invited_by_user_id).first()
            if inviter:
                inviter_name = f"{inviter.FirstName} {inviter.LastName}".strip()

        EmailService.send_invitation_email(email, invitation_link, inviter_name)
        logger.info(f"Invitation email sent to {email}")

        return invitation_token

    @staticmethod
    def accept_invitation(
        session: Session,
        token: str,
        password: str,
        first_name: str = None,
        last_name: str = None
    ) -> User:
        """Accept user invitation"""
        # Verify invitation token
        payload = JWTService.verify_token(token, "invitation")
        if not payload:
            raise NotFound("Invalid or expired invitation token")

        user_id = payload.get("sub")
        email = payload.get("email")
        role_ids = payload.get("role_ids", [])

        # Check if token is revoked
        if JWTService.is_token_revoked(token, session):
            raise NotFound("Invitation token has been revoked")

        # Get user
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFound("User not found")

        if user.IsActive:
            raise Conflict("Invitation already accepted")

        # Update user
        user.Password = AuthService.hash_password(password)
        user.FirstName = first_name or user.FirstName
        user.LastName = last_name or user.LastName
        user.IsActive = True
        user.IsEmailVerified = True

        # Revoke invitation token
        JWTService.revoke_token(token, session)

        # TODO: Assign roles from role_ids

        session.commit()

        return user

    @staticmethod
    def send_welcome_email(session: Session, user_id: str):
        """Send welcome/onboarding email to new user"""
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFound("User not found")

        # Send actual welcome email
        user_name = f"{user.FirstName} {user.LastName}".strip() if user.FirstName else None
        EmailService.send_welcome_email(user.Email, user_name)
        logger.info(f"Welcome email sent to {user.Email}")

    @staticmethod
    def request_password_reset(
        session: Session,
        email: str = None,
        phone: str = None,
        tenant_id: str = None
    ) -> Optional[str]:
        """Request password reset"""
        tenant = AuthService.get_or_create_tenant(session, tenant_id)

        user = None
        if email:
            user = session.query(User).filter(
                func.lower(User.Email) == func.lower(email),
                User.TenantId == tenant.id,
                User.IsActive == True
            ).first()
        elif phone:
            user = session.query(User).filter(
                User.Phone == phone,
                User.TenantId == tenant.id,
                User.IsActive == True
            ).first()

        if not user:
            # For security, don't reveal if user exists
            return None

        # Revoke existing password reset tokens
        JWTService.revoke_all_user_tokens(user.id, session, "password_reset")

        # Create password reset token
        reset_token = JWTService.create_special_token(
            user_id=user.id,
            tenant_id=tenant.id,
            token_type="password_reset",
            session=session,
            expires_hours=settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS,
            additional_claims={
                "email": user.Email,
                "phone": user.Phone
            }
        )

        # Send actual password reset email/SMS
        reset_link = f"{settings.BASE_URL}/auth/reset-password?token={reset_token}"
        if email:
            EmailService.send_password_reset_email(email, reset_link)
            logger.info(f"Password reset email sent to {email}")
        elif phone:
            SMSService.send_password_reset_sms(phone, reset_link)
            logger.info(f"Password reset SMS sent to {phone}")

        return reset_token

    @staticmethod
    def reset_password(session: Session, token: str, new_password: str) -> bool:
        """Reset user password using token"""
        # Verify reset token
        payload = JWTService.verify_token(token, "password_reset")
        if not payload:
            return False

        user_id = payload.get("sub")

        # Check if token is revoked
        if JWTService.is_token_revoked(token, session):
            return False

        # Get user
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Update password
        user.Password = AuthService.hash_password(new_password)
        user.FailedLoginAttempts = 0
        user.LockedUntil = None

        # Revoke the reset token and all user sessions
        JWTService.revoke_token(token, session)
        JWTService.revoke_all_user_tokens(user_id, session, "refresh")

        session.commit()

        return True

    @staticmethod
    def change_password(
        session: Session,
        user_id: str,
        current_password: str,
        new_password: str
    ) -> bool:
        """Change user password"""
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Verify current password
        if not user.Password or not AuthService.verify_password(current_password, user.Password):
            return False

        # Update password
        user.Password = AuthService.hash_password(new_password)

        # Revoke all refresh tokens (force re-login on all devices)
        JWTService.revoke_all_user_tokens(user_id, session, "refresh")

        session.commit()

        return True

    @staticmethod
    def send_email_verification(session: Session, user_id: str) -> str:
        """Send email verification"""
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFound("User not found")

        if user.IsEmailVerified:
            raise Conflict("Email already verified")

        # Revoke existing email verification tokens
        JWTService.revoke_all_user_tokens(user_id, session, "email_verification")

        # Create verification token
        verification_token = JWTService.create_special_token(
            user_id=user.id,
            tenant_id=user.TenantId,
            token_type="email_verification",
            session=session,
            expires_hours=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS,
            additional_claims={"email": user.Email}
        )

        # Send actual verification email
        verification_link = f"{settings.BASE_URL}/auth/verify-email?token={verification_token}"
        EmailService.send_verification_email(user.Email, verification_link)
        logger.info(f"Email verification sent to {user.Email}")

        return verification_token

    @staticmethod
    def verify_email(session: Session, token: str) -> bool:
        """Verify user email using token"""
        # Verify token
        payload = JWTService.verify_token(token, "email_verification")
        if not payload:
            return False

        user_id = payload.get("sub")

        # Check if token is revoked
        if JWTService.is_token_revoked(token, session):
            return False

        # Get user
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Mark email as verified
        user.IsEmailVerified = True

        # Revoke verification token
        JWTService.revoke_token(token, session)

        session.commit()

        return True

    @staticmethod
    def send_phone_verification_otp(session: Session, user_id: str) -> str:
        """Send phone verification OTP"""
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFound("User not found")

        if not user.Phone:
            raise Conflict("No phone number associated with user")

        if user.IsPhoneVerified:
            raise Conflict("Phone already verified")

        # Generate and send OTP
        otp_code = AuthService.generate_otp(
            session, user_id, "phone_verification", user.Phone
        )

        # Send actual SMS
        SMSService.send_phone_verification_sms(user.Phone, otp_code)
        logger.info(f"Phone verification OTP sent to {user.Phone}")

        return otp_code

    @staticmethod
    def verify_phone(session: Session, user_id: str, otp_code: str) -> bool:
        """Verify user phone using OTP"""
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Verify OTP
        if not AuthService.verify_otp(session, user_id, otp_code, "phone_verification"):
            return False

        # Mark phone as verified
        user.IsPhoneVerified = True
        session.commit()

        return True
