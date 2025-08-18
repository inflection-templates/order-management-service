"""
JWT Service - Compatibility layer for the restructured JWT system

This file maintains backward compatibility while delegating to the new
restructured JWT services.
"""

from datetime import timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

# Import the new restructured services
from .jwt_token_service import JWTTokenService
from .jwt_handler import JWTHandler

class JWTService:
    """
    Compatibility layer that delegates to the new JWT services.

    This maintains backward compatibility for existing code while using
    the new restructured JWT system under the hood.
    """

    @staticmethod
    def create_access_token(
        user_id: str,
        tenant_id: str,
        roles: Optional[List[str]] = None,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        return JWTTokenService.create_access_token(
            user_id=user_id,
            tenant_id=tenant_id,
            roles=roles,
            expires_delta=expires_delta
        )

    @staticmethod
    def create_refresh_token(
        user_id: str,
        tenant_id: str,
        session: Session,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT refresh token and store in database"""
        return JWTTokenService.create_refresh_token(
            user_id=user_id,
            tenant_id=tenant_id,
            session=session,
            expires_delta=expires_delta
        )

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload"""
        if token_type == "access":
            return JWTTokenService.verify_access_token(token)
        else:
            # For other token types, we need a session to check revocation
            # This is a limitation of the compatibility layer
            return JWTHandler.verify_token(token, expected_type=token_type)

    @staticmethod
    def create_special_token(
        user_id: str,
        tenant_id: str,
        token_type: str,
        session: Session,
        expires_hours: int = 24,
        additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create special tokens for password reset, email verification, etc."""
        if token_type == "reset_password":
            return JWTTokenService.create_password_reset_token(
                user_id=user_id,
                tenant_id=tenant_id,
                session=session,
                expires_hours=expires_hours
            )
        elif token_type == "verify_email":
            email = additional_claims.get("email", "") if additional_claims else ""
            return JWTTokenService.create_email_verification_token(
                user_id=user_id,
                tenant_id=tenant_id,
                email=email,
                session=session,
                expires_hours=expires_hours
            )
        elif token_type == "invitation":
            email = additional_claims.get("email", "") if additional_claims else ""
            invited_by = additional_claims.get("invited_by", "") if additional_claims else ""
            return JWTTokenService.create_invitation_token(
                user_id=user_id,
                tenant_id=tenant_id,
                email=email,
                invited_by=invited_by,
                session=session,
                expires_hours=expires_hours
            )
        else:
            # For custom token types, use the handler directly
            from datetime import datetime
            payload = {
                "sub": user_id,
                "tenant_id": tenant_id
            }
            if additional_claims:
                payload.update(additional_claims)

            expires_delta = timedelta(hours=expires_hours)
            token = JWTHandler.create_token(
                payload=payload,
                expires_delta=expires_delta,
                token_type=token_type
            )

            # Store in database using token manager
            from .token_manager import TokenManager
            expires_at = datetime.utcnow() + expires_delta
            TokenManager.store_special_token(
                user_id=user_id,
                token=token,
                token_type=token_type,
                expires_at=expires_at,
                session=session
            )

            return token

    @staticmethod
    def revoke_token(token: str, session: Session) -> bool:
        """Revoke a token"""
        return JWTTokenService.revoke_token(token, session)

    @staticmethod
    def is_token_revoked(token: str, session: Session) -> bool:
        """Check if token is revoked"""
        from .token_manager import TokenManager
        return TokenManager.is_token_revoked(token, session)

    @staticmethod
    def revoke_all_user_tokens(user_id: str, session: Session, token_type: Optional[str] = None):
        """Revoke all tokens for a user"""
        return JWTTokenService.revoke_user_tokens(user_id, session, token_type)
