"""
Authorization Examples - Comprehensive usage examples for authenticate_user and authorize_user decorators

This file demonstrates various authorization patterns using the new decorators.
"""

from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.authenticate_decorator import authenticate_user
from app.auth.authorization_decorator import authorize_user
from app.auth.decorators import AuthContext
from app.database.models.order import Order
from app.database.models.user import User
from typing import Dict, Any


# Example 1: Basic RBAC with roles
@authenticate_user(required=True)
@authorize_user(roles=["admin", "manager"])
async def admin_only_endpoint(
    request: Request, 
    db_session: Session,
    auth_context: AuthContext = None
):
    """Only admins and managers can access this endpoint"""
    return {
        "message": "Admin access granted",
        "user_id": auth_context.user_id,
        "roles": auth_context.roles
    }


# Example 2: Permission-based access
@authenticate_user(required=True)
@authorize_user(permissions=["user:read", "user:write"], permission_scope="user_management")
async def user_management_endpoint(
    request: Request,
    db_session: Session, 
    auth_context: AuthContext = None
):
    """Requires specific permissions for user management"""
    return {"message": "User management access granted"}


# Example 3: Ownership-based access
async def load_order_resource(order_id: str, **kwargs) -> Dict[str, Any]:
    """Resource loader function for order ownership checks"""
    db_session = kwargs.get('db_session')
    order = db_session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {
        "id": order.id,
        "user_id": order.UserId,  # Assuming Order has UserId field
        "status": order.Status,
        "created_at": order.CreatedAt
    }


@authenticate_user(required=True)
@authorize_user(
    ownership_check=True,
    ownership_field="user_id",
    resource_loader=load_order_resource
)
async def update_user_order(
    order_id: str,
    request: Request,
    db_session: Session,
    auth_context: AuthContext = None
):
    """Users can only update their own orders"""
    return {
        "message": f"Order {order_id} updated successfully",
        "user_id": auth_context.user_id
    }


# Example 4: ABAC (Attribute-Based Access Control)
finance_policy = {
    "logic": "and",
    "rules": [
        {
            "logic": "and", 
            "conditions": [
                {"attribute": "user.Email", "operator": "regex", "value": r".*@finance\.company\.com$"},
                {"attribute": "time.hour", "operator": "greater_than", "value": 8},
                {"attribute": "time.hour", "operator": "less_than", "value": 18}
            ]
        }
    ]
}

@authenticate_user(required=True)
@authorize_user(abac_policy=finance_policy)
async def finance_report_endpoint(
    request: Request,
    db_session: Session,
    auth_context: AuthContext = None
):
    """Finance reports only accessible during business hours by finance team"""
    return {
        "message": "Finance report access granted",
        "user_email": auth_context.user.Email,
        "access_time": "Business hours"
    }


# Example 5: Complex combined authorization
async def load_sensitive_resource(resource_id: str, **kwargs) -> Dict[str, Any]:
    """Load sensitive resource with multiple attributes"""
    # This would typically load from database
    return {
        "id": resource_id,
        "user_id": "some-user-id",
        "classification": "confidential",
        "department": "hr"
    }

hr_confidential_policy = {
    "logic": "and",
    "rules": [
        {
            "logic": "or",
            "conditions": [
                {"attribute": "user.Email", "operator": "regex", "value": r".*@hr\.company\.com$"},
                {"attribute": "resource.department", "operator": "equals", "value": "hr"}
            ]
        },
        {
            "logic": "and",
            "conditions": [
                {"attribute": "request.method", "operator": "in", "value": ["GET", "POST"]},
                {"attribute": "time.day_of_week", "operator": "less_than", "value": 5}  # Weekdays only
            ]
        }
    ]
}

@authenticate_user(required=True)
@authorize_user(
    roles=["hr_manager", "admin"],
    permissions=["hr:confidential:read"],
    ownership_check=True,
    ownership_field="user_id", 
    consent_required="data_processing",
    abac_policy=hr_confidential_policy,
    resource_loader=load_sensitive_resource
)
async def access_hr_confidential_data(
    resource_id: str,
    request: Request,
    db_session: Session,
    auth_context: AuthContext = None
):
    """
    Complex authorization example:
    - Must be HR manager or admin (RBAC roles)
    - Must have confidential read permission (RBAC permissions)
    - Must own the resource or be authorized (ownership)
    - Must have given data processing consent
    - Must meet ABAC policy conditions (HR email or HR department, weekdays only, etc.)
    """
    return {
        "message": "Access to confidential HR data granted",
        "resource_id": resource_id,
        "user_id": auth_context.user_id
    }


# Example 6: Optional authentication with conditional authorization
@authenticate_user(required=False)
@authorize_user(roles=["premium_user"])
async def premium_feature_endpoint(
    request: Request,
    db_session: Session,
    auth_context: AuthContext = None
):
    """
    Premium feature that's available to authenticated premium users,
    but shows different content for unauthenticated users
    """
    if auth_context:
        # User is authenticated and has premium role
        return {
            "message": "Premium feature access",
            "premium_content": "Advanced analytics data...",
            "user_id": auth_context.user_id
        }
    else:
        # Unauthenticated user gets basic content
        return {
            "message": "Basic feature access",
            "basic_content": "Limited analytics data...",
            "upgrade_prompt": "Sign up for premium features!"
        }


# Example 7: Time-based access control
time_restricted_policy = {
    "logic": "and",
    "rules": [
        {
            "logic": "and",
            "conditions": [
                {"attribute": "time.hour", "operator": "greater_than", "value": 6},
                {"attribute": "time.hour", "operator": "less_than", "value": 22},
                {"attribute": "time.day_of_week", "operator": "less_than", "value": 6}  # Mon-Sat
            ]
        }
    ]
}

@authenticate_user(required=True)
@authorize_user(
    roles=["operator"],
    abac_policy=time_restricted_policy
)
async def system_maintenance_endpoint(
    request: Request,
    db_session: Session,
    auth_context: AuthContext = None
):
    """System maintenance only allowed during specific hours and days"""
    return {
        "message": "System maintenance access granted",
        "operator": auth_context.user.Email,
        "timestamp": "Current time within allowed window"
    }


# Example 8: IP-based access control
ip_restricted_policy = {
    "logic": "and",
    "rules": [
        {
            "logic": "or",
            "conditions": [
                {"attribute": "request.ip", "operator": "regex", "value": r"^192\.168\.1\..*"},
                {"attribute": "request.ip", "operator": "equals", "value": "10.0.0.100"}
            ]
        }
    ]
}

@authenticate_user(required=True)
@authorize_user(
    permissions=["admin:system"],
    abac_policy=ip_restricted_policy
)
async def admin_panel_endpoint(
    request: Request,
    db_session: Session,
    auth_context: AuthContext = None
):
    """Admin panel only accessible from specific IP addresses"""
    return {
        "message": "Admin panel access granted",
        "admin_user": auth_context.user.Email,
        "client_ip": request.client.host if request.client else "unknown"
    }


# Example 9: Resource-specific permissions
async def load_project_resource(project_id: str, **kwargs) -> Dict[str, Any]:
    """Load project with team information"""
    # This would load from database
    return {
        "id": project_id,
        "name": "Sample Project",
        "team_id": "team-123",
        "status": "active",
        "owner_id": "user-456"
    }

@authenticate_user(required=True)
@authorize_user(
    permissions=["project:write"],
    ownership_check=True,
    ownership_field="owner_id",
    resource_loader=load_project_resource
)
async def update_project_endpoint(
    project_id: str,
    request: Request,
    db_session: Session,
    auth_context: AuthContext = None
):
    """Update project - requires write permission and ownership"""
    return {
        "message": f"Project {project_id} updated",
        "updated_by": auth_context.user_id
    }


# Example 10: Nested ownership check
async def load_comment_resource(comment_id: str, **kwargs) -> Dict[str, Any]:
    """Load comment with nested user information"""
    return {
        "id": comment_id,
        "content": "Sample comment",
        "author": {
            "user_id": "user-789",
            "email": "author@example.com"
        },
        "post_id": "post-123"
    }

@authenticate_user(required=True)
@authorize_user(
    ownership_check=True,
    ownership_field="author.user_id",  # Nested field access
    resource_loader=load_comment_resource
)
async def delete_comment_endpoint(
    comment_id: str,
    request: Request,
    db_session: Session,
    auth_context: AuthContext = None
):
    """Delete comment - only comment author can delete"""
    return {
        "message": f"Comment {comment_id} deleted",
        "deleted_by": auth_context.user_id
    }
