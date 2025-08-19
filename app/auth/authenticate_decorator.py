from functools import wraps
from typing import Optional, List, Callable, Any
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.auth.jwt_service import JWTService
from app.database.database_accessor import get_db_session
from app.database.models.user import User
from app.database.models.tenant import Tenant
from app.config.config import get_settings
from app.auth.decorators import AuthContext, get_current_user, get_current_user_optional
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

def authenticate_user(
    required: bool = True
):
    """
    Decorator for authenticating users

    Args:
        required: Whether authentication is required (default: True)

    Usage:
        @authenticate_user(required=True)
        async def protected_endpoint(request: Request, auth_context: AuthContext = None):
            user = auth_context.user
            return {"user_id": user.id}

        @authenticate_user(required=False)
        async def public_endpoint(request: Request, auth_context: AuthContext = None):
            if auth_context:
                return {"message": f"Hello {auth_context.user.FirstName}"}
            return {"message": "Hello anonymous user"}
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request, session, and auth context from kwargs
            request = kwargs.get('request')
            session = kwargs.get('db_session')

            if not request or not session:
                # Try to find them in args (for different parameter orders)
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                    elif isinstance(arg, Session):
                        session = arg

            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )

            if not session:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database session not found"
                )

            # Get authentication credentials
            auth_header = request.headers.get("Authorization")
            credentials = None
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]  # Remove "Bearer " prefix
                credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

            # Get current user
            if required:
                if not credentials:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Authentication required",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                auth_context = await get_current_user(request, credentials, session)
            else:
                auth_context = await get_current_user_optional(request, credentials, session)



            # Add auth_context to kwargs
            kwargs['auth_context'] = auth_context

            return await func(*args, **kwargs)

        return wrapper
    return decorator
