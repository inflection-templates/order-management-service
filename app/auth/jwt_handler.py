"""
JWT Token Handler - Simplified JWT operations without database dependencies
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uuid

# Simplified JWT import - use PyJWT directly
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    jwt = None

from app.config.config import get_settings

settings = get_settings()


class JWTHandler:
    """Handles JWT token creation and verification without database dependencies"""

    @staticmethod
    def _ensure_jwt_available():
        """Ensure JWT library is available"""
        if not JWT_AVAILABLE:
            raise ImportError(
                "PyJWT is required for JWT functionality. "
                "Install it with: pip install PyJWT"
            )

    @staticmethod
    def create_token(
        payload: Dict[str, Any],
        expires_delta: Optional[timedelta] = None,
        token_type: str = "access"
    ) -> str:
        """Create a JWT token with the given payload"""
        JWTHandler._ensure_jwt_available()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            # Default expiry based on token type
            if token_type == "access":
                expire = datetime.utcnow() + timedelta(
                    minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
                )
            elif token_type == "refresh":
                expire = datetime.utcnow() + timedelta(
                    days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
                )
            else:
                expire = datetime.utcnow() + timedelta(hours=24)

        # Add standard claims
        payload.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": token_type
        })

        # Add unique token ID for refresh tokens
        if token_type in ["refresh", "reset_password", "verify_email", "invitation"]:
            payload["jti"] = str(uuid.uuid4())

        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def verify_token(token: str, expected_type: str = None) -> Optional[Dict[str, Any]]:
        """Verify a JWT token and return its payload"""
        JWTHandler._ensure_jwt_available()

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )

            # Check token type if specified
            if expected_type and payload.get("type") != expected_type:
                return None

            return payload

        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.InvalidTokenError:
            # Token is invalid
            return None
        except Exception:
            # Any other error
            return None

    @staticmethod
    def decode_token_without_verification(token: str) -> Optional[Dict[str, Any]]:
        """Decode token without verification (for debugging/inspection)"""
        JWTHandler._ensure_jwt_available()

        try:
            return jwt.decode(
                token,
                options={"verify_signature": False, "verify_exp": False}
            )
        except Exception:
            return None

    @staticmethod
    def get_token_expiry(token: str) -> Optional[datetime]:
        """Get the expiry time of a token"""
        payload = JWTHandler.decode_token_without_verification(token)
        if payload and "exp" in payload:
            return datetime.utcfromtimestamp(payload["exp"])
        return None

    @staticmethod
    def is_token_expired(token: str) -> bool:
        """Check if a token is expired"""
        expiry = JWTHandler.get_token_expiry(token)
        if expiry:
            return datetime.utcnow() > expiry
        return True
