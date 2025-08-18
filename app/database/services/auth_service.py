from sqlalchemy.orm import Session
from app.database.models.auth import Auth
from app.database.models.users import User
from app.domain_types.miscellaneous.exceptions import Unauthorized, NotFound
from app.database.services.users_service import get_user_by_email, verify_password


def authenticate_user(session: Session, email: str, password: str) -> User:
    """Authenticate user with email and password"""
    # Get user by email from Users table
    user = get_user_by_email(session, email)
    if not user:
        raise NotFound(f"User with email '{email}' not found")
    
    # Verify password
    if not verify_password(password, user.Password):
        raise Unauthorized("Invalid password")
    
    return user
