"""
JWT Token Service - Main service combining token handling and database operations
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from .jwt_handler import JWTHandler
from .token_manager import TokenManager
from app.config.config import get_settings

settings = get_settings()


class JWTTokenService:
    """Main JWT service providing all token operations"""

    @staticmethod
    def create_access_token(
        user_id: str,
        tenant_id: str,
        roles: Optional[List[str]] = None,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create an access token"""
        payload = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "roles": roles or []
        }

        return JWTHandler.create_token(
            payload=payload,
            expires_delta=expires_delta,
            token_type="access"
        )

    @staticmethod
    def create_refresh_token(
        user_id: str,
        tenant_id: str,
        session: Session,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a refresh token and store it in database"""
        payload = {
            "sub": user_id,
            "tenant_id": tenant_id
        }

        if expires_delta:
            expires_at = datetime.utcnow() + expires_delta
        else:
            expires_at = datetime.utcnow() + timedelta(
                days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
            )

        token = JWTHandler.create_token(
            payload=payload,
            expires_delta=expires_delta,
            token_type="refresh"
        )

        # Store in database
        TokenManager.store_refresh_token(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            session=session
        )

        return token

    @staticmethod
    def create_password_reset_token(
        user_id: str,
        tenant_id: str,
        session: Session,
        expires_hours: int = None
    ) -> str:
        """Create a password reset token"""
        if expires_hours is None:
            expires_hours = settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS

        payload = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "purpose": "password_reset"
        }

        expires_delta = timedelta(hours=expires_hours)
        expires_at = datetime.utcnow() + expires_delta

        token = JWTHandler.create_token(
            payload=payload,
            expires_delta=expires_delta,
            token_type="reset_password"
        )

        # Store in database
        TokenManager.store_special_token(
            user_id=user_id,
            token=token,
            token_type="reset_password",
            expires_at=expires_at,
            session=session
        )

        return token

    @staticmethod
    def create_email_verification_token(
        user_id: str,
        tenant_id: str,
        email: str,
        session: Session,
        expires_hours: int = None
    ) -> str:
        """Create an email verification token"""
        if expires_hours is None:
            expires_hours = settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS

        payload = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "email": email,
            "purpose": "email_verification"
        }

        expires_delta = timedelta(hours=expires_hours)
        expires_at = datetime.utcnow() + expires_delta

        token = JWTHandler.create_token(
            payload=payload,
            expires_delta=expires_delta,
            token_type="verify_email"
        )

        # Store in database
        TokenManager.store_special_token(
            user_id=user_id,
            token=token,
            token_type="verify_email",
            expires_at=expires_at,
            session=session
        )

        return token

    @staticmethod
    def create_invitation_token(
        user_id: str,
        tenant_id: str,
        email: str,
        invited_by: str,
        session: Session,
        expires_hours: int = 72  # 3 days default
    ) -> str:
        """Create an invitation token"""
        payload = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "email": email,
            "invited_by": invited_by,
            "purpose": "invitation"
        }

        expires_delta = timedelta(hours=expires_hours)
        expires_at = datetime.utcnow() + expires_delta

        token = JWTHandler.create_token(
            payload=payload,
            expires_delta=expires_delta,
            token_type="invitation"
        )

        # Store in database
        TokenManager.store_special_token(
            user_id=user_id,
            token=token,
            token_type="invitation",
            expires_at=expires_at,
            session=session
        )

        return token

    @staticmethod
    def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify an access token"""
        return JWTHandler.verify_token(token, expected_type="access")

    @staticmethod
    def verify_refresh_token(token: str, session: Session) -> Optional[Dict[str, Any]]:
        """Verify a refresh token and check if it's revoked"""
        payload = JWTHandler.verify_token(token, expected_type="refresh")

        if payload and not TokenManager.is_token_revoked(token, session):
            return payload

        return None

    @staticmethod
    def verify_special_token(
        token: str,
        token_type: str,
        session: Session
    ) -> Optional[Dict[str, Any]]:
        """Verify special tokens (password reset, email verification, etc.)"""
        payload = JWTHandler.verify_token(token, expected_type=token_type)

        if payload and not TokenManager.is_token_revoked(token, session):
            return payload

        return None

    @staticmethod
    def revoke_token(token: str, session: Session) -> bool:
        """Revoke a specific token"""
        return TokenManager.revoke_token(token, session)

    @staticmethod
    def revoke_user_tokens(
        user_id: str,
        session: Session,
        token_type: Optional[str] = None
    ) -> int:
        """Revoke all tokens for a user"""
        return TokenManager.revoke_user_tokens(user_id, session, token_type)

    @staticmethod
    def refresh_access_token(
        refresh_token: str,
        session: Session
    ) -> Optional[Dict[str, str]]:
        """Create new access token using refresh token"""
        payload = JWTTokenService.verify_refresh_token(refresh_token, session)

        if not payload:
            return None

        user_id = payload.get("sub")
        tenant_id = payload.get("tenant_id")

        if not user_id or not tenant_id:
            return None

        # Get user roles (you might want to fetch fresh roles from database)
        roles = []  # TODO: Fetch user roles from database

        new_access_token = JWTTokenService.create_access_token(
            user_id=user_id,
            tenant_id=tenant_id,
            roles=roles
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    @staticmethod
    def get_user_active_sessions(user_id: str, session: Session) -> List[dict]:
        """Get active sessions (refresh tokens) for a user"""
        return TokenManager.get_user_active_tokens(
            user_id=user_id,
            session=session,
            token_type="refresh"
        )

    @staticmethod
    def cleanup_expired_tokens(session: Session) -> int:
        """Clean up expired tokens from database"""
        return TokenManager.cleanup_expired_tokens(session)
