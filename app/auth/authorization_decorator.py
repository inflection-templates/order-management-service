"""
Authorization Decorator - Comprehensive user authorization with RBAC, ownership, consent, and ABAC

This module provides the authorize_user decorator and all related authorization functionality,
separated from authentication concerns.
"""

from functools import wraps
from typing import Optional, List, Callable, Any, Dict
from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database.models.role import Role, RolePermission
from app.database.models.user_role import UserRole
from app.auth.decorators import AuthContext
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


# Authorization Helper Classes and Functions

class AuthorizationContext:
    """Context for authorization decisions"""
    def __init__(self, auth_context: AuthContext, session: Session, request: Request, resource_data: Dict = None):
        self.auth_context = auth_context
        self.session = session
        self.request = request
        self.resource_data = resource_data or {}
        self.user = auth_context.user
        self.tenant = auth_context.tenant
        self.user_id = auth_context.user_id
        self.tenant_id = auth_context.tenant_id


def check_rbac_roles(auth_context: AuthContext, required_roles: List[str], session: Session) -> bool:
    """Check if user has required roles"""
    if not required_roles:
        return True
    
    # Get user roles from database
    user_roles = session.query(UserRole).join(Role).filter(
        UserRole.UserId == auth_context.user_id,
        UserRole.DeletedAt.is_(None),
        Role.id == UserRole.RoleId
    ).all()
    
    user_role_names = [ur.role.RoleName for ur in user_roles if ur.role]
    
    # Check if user has any of the required roles
    return any(role in user_role_names for role in required_roles)


def check_rbac_permissions(auth_context: AuthContext, required_permissions: List[str], session: Session, scope: str = "global") -> bool:
    """Check if user has required permissions"""
    if not required_permissions:
        return True
    
    # Get user permissions through roles
    permissions = session.query(RolePermission).join(UserRole).filter(
        UserRole.UserId == auth_context.user_id,
        UserRole.DeletedAt.is_(None),
        RolePermission.RoleId == UserRole.RoleId,
        RolePermission.Enabled == True,
        RolePermission.DeletedAt.is_(None),
        or_(RolePermission.Scope == scope, RolePermission.Scope == "global")
    ).all()
    
    user_permissions = [perm.Privilege for perm in permissions]
    
    # Check if user has any of the required permissions
    return any(perm in user_permissions for perm in required_permissions)


def check_ownership(auth_context: AuthContext, resource_data: Dict, ownership_field: str = "user_id") -> bool:
    """Check if user owns the resource"""
    if not resource_data:
        return False
    
    # Support nested field access (e.g., "user.id", "created_by.user_id")
    field_parts = ownership_field.split(".")
    value = resource_data
    
    try:
        for part in field_parts:
            if hasattr(value, part):
                value = getattr(value, part)
            elif isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return False
        
        return str(value) == str(auth_context.user_id)
    except (AttributeError, KeyError, TypeError):
        return False


def check_consent(auth_context: AuthContext, consent_type: str, resource_data: Dict, session: Session) -> bool:
    """Check if user has given consent for the operation"""
    # This is a placeholder - implement based on your consent model
    # You might have a separate consent table to track user consents
    
    # Example implementation:
    # consent = session.query(UserConsent).filter(
    #     UserConsent.UserId == auth_context.user_id,
    #     UserConsent.ConsentType == consent_type,
    #     UserConsent.IsActive == True
    # ).first()
    # return consent is not None
    
    # For now, return True (implement based on your requirements)
    return True


def evaluate_abac_policy(auth_context: AuthorizationContext, policy: Dict) -> bool:
    """Evaluate Attribute-Based Access Control policy"""
    
    def evaluate_condition(condition: Dict) -> bool:
        """Evaluate a single condition"""
        operator = condition.get("operator")
        attribute = condition.get("attribute")
        value = condition.get("value")
        
        # Get attribute value from context
        attr_value = get_attribute_value(auth_context, attribute)
        
        if operator == "equals":
            return attr_value == value
        elif operator == "not_equals":
            return attr_value != value
        elif operator == "in":
            return attr_value in value if isinstance(value, list) else False
        elif operator == "not_in":
            return attr_value not in value if isinstance(value, list) else True
        elif operator == "greater_than":
            try:
                return float(attr_value) > float(value)
            except (ValueError, TypeError):
                return False
        elif operator == "less_than":
            try:
                return float(attr_value) < float(value)
            except (ValueError, TypeError):
                return False
        elif operator == "regex":
            try:
                return bool(re.match(value, str(attr_value)))
            except (TypeError, re.error):
                return False
        elif operator == "exists":
            return attr_value is not None
        elif operator == "not_exists":
            return attr_value is None
        else:
            return False
    
    def evaluate_rule(rule: Dict) -> bool:
        """Evaluate a rule with conditions"""
        conditions = rule.get("conditions", [])
        logic = rule.get("logic", "and")  # "and" or "or"
        
        if not conditions:
            return True
        
        results = [evaluate_condition(cond) for cond in conditions]
        
        if logic == "and":
            return all(results)
        elif logic == "or":
            return any(results)
        else:
            return False
    
    # Evaluate all rules in the policy
    rules = policy.get("rules", [])
    policy_logic = policy.get("logic", "and")
    
    if not rules:
        return True
    
    rule_results = [evaluate_rule(rule) for rule in rules]
    
    if policy_logic == "and":
        return all(rule_results)
    elif policy_logic == "or":
        return any(rule_results)
    else:
        return False


def get_attribute_value(auth_context: AuthorizationContext, attribute: str) -> Any:
    """Get attribute value from authorization context"""
    
    # Support dot notation for nested attributes
    parts = attribute.split(".")
    
    # User attributes
    if parts[0] == "user":
        obj = auth_context.user
        for part in parts[1:]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return None
        return obj
    
    # Tenant attributes
    elif parts[0] == "tenant":
        obj = auth_context.tenant
        for part in parts[1:]:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return None
        return obj
    
    # Request attributes
    elif parts[0] == "request":
        if len(parts) == 2:
            if parts[1] == "method":
                return auth_context.request.method
            elif parts[1] == "path":
                return auth_context.request.url.path
            elif parts[1] == "ip":
                return auth_context.request.client.host if auth_context.request.client else None
        return None
    
    # Resource attributes
    elif parts[0] == "resource":
        obj = auth_context.resource_data
        for part in parts[1:]:
            if isinstance(obj, dict) and part in obj:
                obj = obj[part]
            elif hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                return None
        return obj
    
    # Time attributes
    elif parts[0] == "time":
        now = datetime.now()
        if len(parts) == 2:
            if parts[1] == "hour":
                return now.hour
            elif parts[1] == "day_of_week":
                return now.weekday()
            elif parts[1] == "timestamp":
                return now.timestamp()
        return None
    
    return None


def authorize_user(
    roles: Optional[List[str]] = None,
    permissions: Optional[List[str]] = None,
    permission_scope: str = "global",
    ownership_check: bool = False,
    ownership_field: str = "user_id",
    consent_required: Optional[str] = None,
    abac_policy: Optional[Dict] = None,
    resource_loader: Optional[Callable] = None
):
    """
    Decorator for comprehensive user authorization with RBAC, ownership, consent, and ABAC
    
    Args:
        roles: List of required roles (RBAC)
        permissions: List of required permissions (RBAC) 
        permission_scope: Scope for permission checking (default: "global")
        ownership_check: Whether to check resource ownership
        ownership_field: Field name to check for ownership (supports dot notation)
        consent_required: Type of consent required for the operation
        abac_policy: Attribute-Based Access Control policy dictionary
        resource_loader: Function to load resource data for ownership/ABAC checks
    
    RBAC Usage:
        @authorize_user(roles=["admin", "manager"])
        async def admin_endpoint(request: Request, auth_context: AuthContext = None):
            return {"message": "Admin access granted"}
        
        @authorize_user(permissions=["user:read", "user:write"])
        async def user_management(request: Request, auth_context: AuthContext = None):
            return {"message": "User management access"}
    
    Ownership Usage:
        @authorize_user(ownership_check=True, ownership_field="created_by")
        async def update_order(order_id: str, request: Request, auth_context: AuthContext = None):
            # Will check if auth_context.user_id matches resource.created_by
            return {"message": "Order updated"}
    
    ABAC Usage:
        policy = {
            "logic": "and",
            "rules": [
                {
                    "logic": "and",
                    "conditions": [
                        {"attribute": "user.department", "operator": "equals", "value": "finance"},
                        {"attribute": "time.hour", "operator": "greater_than", "value": 9},
                        {"attribute": "time.hour", "operator": "less_than", "value": 17}
                    ]
                }
            ]
        }
        
        @authorize_user(abac_policy=policy)
        async def finance_report(request: Request, auth_context: AuthContext = None):
            return {"message": "Finance report access"}
    
    Combined Usage:
        @authorize_user(
            roles=["user"],
            ownership_check=True,
            consent_required="data_processing",
            abac_policy={"rules": [...]}
        )
        async def complex_endpoint(request: Request, auth_context: AuthContext = None):
            return {"message": "Complex authorization passed"}
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get auth_context from kwargs (should be set by authenticate_user decorator)
            auth_context = kwargs.get('auth_context')
            if not auth_context:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required before authorization"
                )
            
            # Get database session
            session = kwargs.get('db_session')
            if not session:
                # Try to find it in args
                for arg in args:
                    if isinstance(arg, Session):
                        session = arg
                        break
            
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database session not found"
                )
            
            # Get request object
            request = kwargs.get('request')
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )
            
            # Load resource data if needed
            resource_data = {}
            if (ownership_check or abac_policy) and resource_loader:
                try:
                    resource_data = await resource_loader(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Failed to load resource data: {e}")
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to load resource for authorization"
                    )
            
            # Create authorization context
            auth_ctx = AuthorizationContext(auth_context, session, request, resource_data)
            
            # RBAC - Check roles
            if roles and not check_rbac_roles(auth_context, roles, session):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Required roles: {', '.join(roles)}"
                )
            
            # RBAC - Check permissions
            if permissions and not check_rbac_permissions(auth_context, permissions, session, permission_scope):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Required permissions: {', '.join(permissions)}"
                )
            
            # Ownership check
            if ownership_check and not check_ownership(auth_context, resource_data, ownership_field):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Resource access denied: ownership required"
                )
            
            # Consent check
            if consent_required and not check_consent(auth_context, consent_required, resource_data, session):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Consent required: {consent_required}"
                )
            
            # ABAC policy evaluation
            if abac_policy and not evaluate_abac_policy(auth_ctx, abac_policy):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied by policy"
                )
            
            # All authorization checks passed
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator
