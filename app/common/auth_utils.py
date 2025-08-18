from datetime import datetime, timedelta
from typing import Optional
import jwt
import hashlib
from fastapi import HTTPException, status
from app.config.config import get_settings
from app.domain_types.schemas.auth import TokenData
from app.domain_types.enums.role_enum import UserRole

settings = get_settings()

# JWT settings
SECRET_KEY = settings.USER_ACCESS_TOKEN_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def verify_token(token: str) -> TokenData:
    """Verify and decode a JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized access.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        
        if user_id is None or email is None or role is None:
            raise credentials_exception
            
        token_data = TokenData(
            user_id=user_id, 
            email=email, 
            role=UserRole(role)
        )
        return token_data
    except jwt.PyJWTError:
        raise credentials_exception


def check_role_permission(current_role: UserRole, required_role: UserRole) -> bool:
    """Check if current role has permission for required role"""
    # Admin has access to everything
    if current_role == UserRole.ADMIN:
        return True
    
    # User can only access user-level resources
    if current_role == UserRole.USER and required_role == UserRole.USER:
        return True
    
    return False
