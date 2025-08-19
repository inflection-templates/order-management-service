"""
Examples of how to use the @authenticate_user decorator

This file contains various examples showing different ways to use the authentication decorator
in your FastAPI routes. Copy these patterns to your own route files.
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database_alchemy.database_accessor import get_db_session
from app.auth import authenticate_user, AuthContext
from app.domain_types.miscellaneous.response_model import ResponseModel
from typing import Dict, Any

router = APIRouter(prefix="/examples", tags=["auth-examples"])

# Example 1: Basic authentication required
@router.get("/protected")
@authenticate_user(required=True)
async def protected_endpoint(
    request: Request,
    db_session: Session = Depends(get_db_session),
    auth_context: AuthContext = None
) -> ResponseModel[Dict[str, Any]]:
    """
    Basic protected endpoint - requires valid JWT token
    """
    user = auth_context.user
    return ResponseModel[Dict[str, Any]](
        Message="Access granted",
        Data={
            "user_id": user.id,
            "user_name": f"{user.FirstName} {user.LastName}",
            "tenant_id": auth_context.tenant_id,
            "roles": auth_context.roles
        }
    )

# Example 2: Role-based access control
@router.get("/admin-only")
@authenticate_user(required=True, roles=["admin"])
async def admin_only_endpoint(
    request: Request,
    db_session: Session = Depends(get_db_session),
    auth_context: AuthContext = None
) -> ResponseModel[Dict[str, str]]:
    """
    Admin-only endpoint - requires 'admin' role
    """
    return ResponseModel[Dict[str, str]](
        Message="Admin access granted",
        Data={"admin_user": auth_context.user.Email}
    )

# Example 3: Multiple roles allowed
@router.get("/staff-area")
@authenticate_user(required=True, roles=["admin", "manager", "staff"])
async def staff_area_endpoint(
    request: Request,
    db_session: Session = Depends(get_db_session),
    auth_context: AuthContext = None
) -> ResponseModel[Dict[str, str]]:
    """
    Staff area - requires admin, manager, or staff role
    """
    return ResponseModel[Dict[str, str]](
        Message="Staff access granted",
        Data={"role": auth_context.roles[0] if auth_context.roles else "unknown"}
    )

# Example 4: Optional authentication (public endpoint with optional user data)
@router.get("/public-with-optional-auth")
@authenticate_user(required=False)
async def public_with_optional_auth(
    request: Request,
    db_session: Session = Depends(get_db_session),
    auth_context: AuthContext = None
) -> ResponseModel[Dict[str, Any]]:
    """
    Public endpoint that shows different content for authenticated users
    """
    if auth_context:
        return ResponseModel[Dict[str, Any]](
            Message=f"Hello {auth_context.user.FirstName}!",
            Data={
                "authenticated": True,
                "user_id": auth_context.user.id,
                "tenant": auth_context.tenant.Name
            }
        )
    else:
        return ResponseModel[Dict[str, Any]](
            Message="Hello anonymous user!",
            Data={"authenticated": False}
        )

# Example 5: Completely public endpoint (no decorator)
@router.get("/completely-public")
async def completely_public_endpoint() -> ResponseModel[Dict[str, str]]:
    """
    Completely public endpoint - no authentication at all
    """
    return ResponseModel[Dict[str, str]](
        Message="This is a public endpoint",
        Data={"public": True}
    )

# Example 6: POST endpoint with authentication
@router.post("/create-resource")
@authenticate_user(required=True, roles=["admin", "manager"])
async def create_resource_endpoint(
    resource_data: Dict[str, Any],
    request: Request,
    db_session: Session = Depends(get_db_session),
    auth_context: AuthContext = None
) -> ResponseModel[Dict[str, Any]]:
    """
    Create a resource - requires admin or manager role
    """
    # Your business logic here
    # You have access to:
    # - auth_context.user (the authenticated user)
    # - auth_context.tenant (the user's tenant)
    # - auth_context.roles (user's roles)
    # - resource_data (the request body)
    # - db_session (database session)

    return ResponseModel[Dict[str, Any]](
        Message="Resource created successfully",
        Data={
            "created_by": auth_context.user.id,
            "tenant_id": auth_context.tenant_id,
            "resource_id": "example-123"
        }
    )

# Example 7: Error handling example
@router.get("/error-example")
@authenticate_user(required=True, roles=["nonexistent-role"])
async def error_example(
    request: Request,
    db_session: Session = Depends(get_db_session),
    auth_context: AuthContext = None
) -> ResponseModel[Dict[str, str]]:
    """
    This will return 403 Forbidden because no user will have 'nonexistent-role'
    """
    return ResponseModel[Dict[str, str]](
        Message="This should not be reached",
        Data={"error": "This endpoint requires a role that doesn't exist"}
    )

"""
Usage in your own routes:

1. Import the decorator:
   from app.auth import authenticate_user, AuthContext

2. Add the decorator to your route:
   @authenticate_user(required=True)  # Basic auth
   @authenticate_user(required=True, roles=["admin"])  # Role-based
   @authenticate_user(required=False)  # Optional auth

3. Add auth_context parameter to your function:
   async def your_endpoint(
       request: Request,
       db_session: Session = Depends(get_db_session),
       auth_context: AuthContext = None  # This will be populated by the decorator
   ):

4. Use the auth context:
   if auth_context:
       user = auth_context.user
       tenant = auth_context.tenant
       roles = auth_context.roles

Common HTTP status codes returned by the decorator:
- 401 Unauthorized: No token provided or invalid token
- 403 Forbidden: Valid token but insufficient roles/permissions
- 500 Internal Server Error: Missing request or database session
"""
