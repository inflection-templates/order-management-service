from functools import wraps
from typing import Optional, List, Callable, Any
from fastapi import HTTPException, status, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.auth.jwt_service import JWTService
from app.database.database_accessor import get_db_session
from app.database.models.user import User
from app.database.models.tenant import Tenant
from app.config.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()
security = HTTPBearer(auto_error=False)

class AuthContext:
    def __init__(self, user: User, tenant: Tenant, roles: List[str] = None):
        self.user = user
        self.tenant = tenant
        self.roles = roles or []
        self.user_id = user.id
        self.tenant_id = tenant.id

def get_tenant_from_request(request: Request) -> Optional[str]:
    """Extract tenant ID from request headers or subdomain"""
    # First try header
    tenant_id = request.headers.get(settings.TENANT_HEADER_NAME)
    if tenant_id:
        return tenant_id

    # Then try subdomain (if using subdomain-based tenancy)
    host = request.headers.get("host", "")
    if "." in host:
        subdomain = host.split(".")[0]
        return subdomain

    # Default tenant
    return settings.DEFAULT_TENANT_ID

async def get_current_user_optional(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_db_session)
) -> Optional[AuthContext]:
    """Get current user without raising exception if not authenticated"""
    if not credentials:
        return None

    try:
        return await get_current_user(request, credentials, session)
    except HTTPException:
        return None

async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_db_session)
) -> AuthContext:
    """Get current authenticated user"""

    token = credentials.credentials if credentials else None
    payload = JWTService.verify_token(token, "access")

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")
    roles = payload.get("roles", [])

    if not user_id or not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify tenant from request matches token
    request_tenant_id = get_tenant_from_request(request)
    if request_tenant_id != tenant_id and request_tenant_id != settings.DEFAULT_TENANT_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant mismatch"
        )

    # Check if token is revoked
    if JWTService.is_token_revoked(token, session):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = session.query(User).filter(
        User.id == user_id,
        User.TenantId == tenant_id,
        User.IsActive == True
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    # Get tenant
    tenant = session.query(Tenant).filter(
        Tenant.id == tenant_id,
        Tenant.IsActive == True
    ).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tenant not found or inactive"
        )

    return AuthContext(user, tenant, roles)

# The authenticate_user decorator has been moved to app/auth/authenticate_decorator.py
# Import it from there: from app.auth.authenticate_decorator import authenticate_user
