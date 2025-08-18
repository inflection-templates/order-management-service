"""
Token Manager - Handles database operations for tokens
"""

from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session

from .jwt_handler import JWTHandler


class TokenManager:
    """Manages token storage and retrieval from database"""

    @staticmethod
    def store_refresh_token(
        user_id: str,
        token: str,
        expires_at: datetime,
        session: Session
    ) -> bool:
        """Store a refresh token in the database"""
        try:
            # Import here to avoid circular imports
            from app.database.models.auth_token import AuthToken

            db_token = AuthToken(
                UserId=user_id,
                TokenType="refresh",
                Token=token,
                ExpiresAt=expires_at,
                IsRevoked=False
            )
            session.add(db_token)
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            print(f"Error storing refresh token: {e}")
            return False

    @staticmethod
    def store_special_token(
        user_id: str,
        token: str,
        token_type: str,
        expires_at: datetime,
        session: Session
    ) -> bool:
        """Store special tokens (password reset, email verification, etc.)"""
        try:
            # Import here to avoid circular imports
            from app.database.models.auth_token import AuthToken

            db_token = AuthToken(
                UserId=user_id,
                TokenType=token_type,
                Token=token,
                ExpiresAt=expires_at,
                IsRevoked=False
            )
            session.add(db_token)
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            print(f"Error storing {token_type} token: {e}")
            return False

    @staticmethod
    def is_token_revoked(token: str, session: Session) -> bool:
        """Check if a token is revoked in the database"""
        try:
            # Import here to avoid circular imports
            from app.database.models.auth_token import AuthToken

            # For access tokens, we don't store them, so they can't be revoked
            payload = JWTHandler.decode_token_without_verification(token)
            if payload and payload.get("type") == "access":
                return False

            # For other tokens, check database
            db_token = session.query(AuthToken).filter(
                AuthToken.Token == token
            ).first()

            if db_token:
                return db_token.IsRevoked

            # If token not found in database, consider it revoked for security
            return True

        except Exception as e:
            print(f"Error checking token revocation: {e}")
            return True

    @staticmethod
    def revoke_token(token: str, session: Session) -> bool:
        """Revoke a specific token"""
        try:
            # Import here to avoid circular imports
            from app.database.models.auth_token import AuthToken

            db_token = session.query(AuthToken).filter(
                AuthToken.Token == token,
                AuthToken.IsRevoked == False
            ).first()

            if db_token:
                db_token.IsRevoked = True
                session.commit()
                return True

            return False

        except Exception as e:
            session.rollback()
            print(f"Error revoking token: {e}")
            return False

    @staticmethod
    def revoke_user_tokens(
        user_id: str,
        session: Session,
        token_type: Optional[str] = None
    ) -> int:
        """Revoke all tokens for a user, optionally filtered by type"""
        try:
            # Import here to avoid circular imports
            from app.database.models.auth_token import AuthToken

            query = session.query(AuthToken).filter(
                AuthToken.UserId == user_id,
                AuthToken.IsRevoked == False
            )

            if token_type:
                query = query.filter(AuthToken.TokenType == token_type)

            tokens = query.all()
            count = len(tokens)

            for token in tokens:
                token.IsRevoked = True

            session.commit()
            return count

        except Exception as e:
            session.rollback()
            print(f"Error revoking user tokens: {e}")
            return 0

    @staticmethod
    def cleanup_expired_tokens(session: Session) -> int:
        """Remove expired tokens from database"""
        try:
            # Import here to avoid circular imports
            from app.database.models.auth_token import AuthToken

            expired_tokens = session.query(AuthToken).filter(
                AuthToken.ExpiresAt < datetime.utcnow()
            ).all()

            count = len(expired_tokens)

            for token in expired_tokens:
                session.delete(token)

            session.commit()
            return count

        except Exception as e:
            session.rollback()
            print(f"Error cleaning up expired tokens: {e}")
            return 0

    @staticmethod
    def get_user_active_tokens(
        user_id: str,
        session: Session,
        token_type: Optional[str] = None
    ) -> List[dict]:
        """Get active tokens for a user"""
        try:
            # Import here to avoid circular imports
            from app.database.models.auth_token import AuthToken

            query = session.query(AuthToken).filter(
                AuthToken.UserId == user_id,
                AuthToken.IsRevoked == False,
                AuthToken.ExpiresAt > datetime.utcnow()
            )

            if token_type:
                query = query.filter(AuthToken.TokenType == token_type)

            tokens = query.all()

            return [
                {
                    "id": token.id,
                    "type": token.TokenType,
                    "created_at": token.CreatedAt,
                    "expires_at": token.ExpiresAt
                }
                for token in tokens
            ]

        except Exception as e:
            print(f"Error getting user active tokens: {e}")
            return []
