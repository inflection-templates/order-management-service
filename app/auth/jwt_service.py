from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import uuid
from sqlalchemy.orm import Session

# Use PyJWT as primary, fallback to python-jose if available
try:
    import jwt
    from jwt.exceptions import InvalidTokenError as JWTError

    # Adapter for PyJWT to provide consistent interface
    class JWTAdapter:
        @staticmethod
        def encode(payload: dict, key: str, algorithm: str = "HS256") -> str:
            return jwt.encode(payload, key, algorithm=algorithm)

        @staticmethod
        def decode(token: str, key: str, algorithms: list = None) -> dict:
            if algorithms is None:
                algorithms = ["HS256"]
            return jwt.decode(token, key, algorithms=algorithms)

    jwt_handler = JWTAdapter()

except ImportError:
    try:
        from jose import JWTError, jwt as jwt_handler
    except ImportError:
        raise ImportError("Either PyJWT or python-jose must be installed for JWT functionality")

from app.config.config import get_settings
from app.database.models.auth_token import AuthToken
from app.database.models.user import User

settings = get_settings()

class JWTService:

    @staticmethod
    def create_access_token(
        user_id: str,
        tenant_id: str,
        roles: list = None,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "roles": roles or [],
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }

        return jwt_handler.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(
        user_id: str,
        tenant_id: str,
        session: Session,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT refresh token and store in database"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

        token_id = str(uuid.uuid4())
        to_encode = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
            "jti": token_id
        }

        token = jwt_handler.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

        # Store refresh token in database
        db_token = AuthToken(
            UserId=user_id,
            TokenType="refresh",
            Token=token,
            ExpiresAt=expire
        )
        session.add(db_token)
        session.commit()

        return token

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt_handler.decode(token, settings.JWT_SECRET_KEY, [settings.JWT_ALGORITHM])

            if payload.get("type") != token_type:
                return None

            return payload
        except JWTError:
            return None

    @staticmethod
    def create_special_token(
        user_id: str,
        tenant_id: str,
        token_type: str,
        session: Session,
        expires_hours: int = 24,
        additional_claims: Dict[str, Any] = None
    ) -> str:
        """Create special tokens for password reset, email verification, etc."""
        expire = datetime.utcnow() + timedelta(hours=expires_hours)
        token_id = str(uuid.uuid4())

        to_encode = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": token_type,
            "jti": token_id
        }

        if additional_claims:
            to_encode.update(additional_claims)

        token = jwt_handler.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

        # Store token in database
        db_token = AuthToken(
            UserId=user_id,
            TokenType=token_type,
            Token=token,
            ExpiresAt=expire
        )
        session.add(db_token)
        session.commit()

        return token

    @staticmethod
    def revoke_token(token: str, session: Session) -> bool:
        """Revoke a token"""
        try:
            payload = jwt_handler.decode(token, settings.JWT_SECRET_KEY, [settings.JWT_ALGORITHM])
            jti = payload.get("jti")

            if jti:
                db_token = session.query(AuthToken).filter(
                    AuthToken.Token == token,
                    AuthToken.IsRevoked == False
                ).first()

                if db_token:
                    db_token.IsRevoked = True
                    session.commit()
                    return True
        except JWTError:
            pass

        return False

    @staticmethod
    def is_token_revoked(token: str, session: Session) -> bool:
        """Check if token is revoked"""
        try:
            payload = jwt_handler.decode(token, settings.JWT_SECRET_KEY, [settings.JWT_ALGORITHM])

            # For access tokens, we don't store them in DB, so they're not revoked
            if payload.get("type") == "access":
                return False

            # For other tokens, check database
            db_token = session.query(AuthToken).filter(
                AuthToken.Token == token
            ).first()

            return db_token.IsRevoked if db_token else True
        except JWTError:
            return True

    @staticmethod
    def revoke_all_user_tokens(user_id: str, session: Session, token_type: str = None):
        """Revoke all tokens for a user"""
        query = session.query(AuthToken).filter(
            AuthToken.UserId == user_id,
            AuthToken.IsRevoked == False
        )

        if token_type:
            query = query.filter(AuthToken.TokenType == token_type)

        tokens = query.all()
        for token in tokens:
            token.IsRevoked = True

        session.commit()
