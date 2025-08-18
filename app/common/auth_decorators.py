import functools
from typing import List, Optional, Callable, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.common.auth_utils import verify_token
from app.domain_types.schemas.auth import TokenData
from app.domain_types.enums.role_enum import UserRole
import inspect

security = HTTPBearer()


def get_current_user_dependency(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """FastAPI dependency for getting current user"""
    return verify_token(credentials.credentials)


def get_current_admin_dependency(current_user: TokenData = Depends(get_current_user_dependency)) -> TokenData:
    """FastAPI dependency for admin users"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden user access."
        )
    return current_user


def get_current_user_role_dependency(current_user: TokenData = Depends(get_current_user_dependency)) -> TokenData:
    """FastAPI dependency for user role only"""
    if current_user.role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden user access."
        )
    return current_user


def get_current_user_or_admin_dependency(current_user: TokenData = Depends(get_current_user_dependency)) -> TokenData:
    """FastAPI dependency for user or admin roles"""
    if current_user.role not in [UserRole.USER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden user access."
        )
    return current_user


def create_role_dependency(*required_roles: UserRole):
    """Create a custom dependency for specific roles"""
    def dependency(current_user: TokenData = Depends(get_current_user_dependency)) -> TokenData:
        if current_user.role not in required_roles:
            role_names = [role.value for role in required_roles]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden user access."
            )
        return current_user
    return dependency


def _add_auth_dependency(func: Callable, dependency_func: Callable) -> Callable:
    """
    Helper function to add authentication dependency to a function.
    Handles cases where current_user parameter already exists or needs to be added.
    """
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    
    # Check if current_user parameter already exists
    current_user_exists = any(param.name == 'current_user' for param in params)
    
    if current_user_exists:
        # Update existing current_user parameter with the new dependency
        new_params = []
        for param in params:
            if param.name == 'current_user':
                new_param = param.replace(
                    default=Depends(dependency_func),
                    annotation=TokenData
                )
                new_params.append(new_param)
            else:
                new_params.append(param)
        params = new_params
    else:
        # Add new current_user parameter
        current_user_param = inspect.Parameter(
            'current_user',
            inspect.Parameter.KEYWORD_ONLY,
            default=Depends(dependency_func),
            annotation=TokenData
        )
        params.append(current_user_param)
    
    # Create new signature
    new_sig = sig.replace(parameters=params)
    func.__signature__ = new_sig
    
    return func


def authenticate_required(func: Callable) -> Callable:
    """
    Decorator that adds authentication to the route function.
    """
    return _add_auth_dependency(func, get_current_user_dependency)


def authenticate_admin(func: Callable) -> Callable:
    """
    Decorator that requires admin role for the route.
    """
    return _add_auth_dependency(func, get_current_admin_dependency)


def authenticate_user(func: Callable) -> Callable:
    """
    Decorator that requires user role for the route.
    """
    return _add_auth_dependency(func, get_current_user_role_dependency)

def require_roles(*required_roles: UserRole):
    """
    Decorator factory that creates a decorator for specific roles.
    """
    def decorator(func: Callable) -> Callable:
        role_dependency = create_role_dependency(*required_roles)
        return _add_auth_dependency(func, role_dependency)
    
    return decorator


# Alias for backward compatibility
auth_required = authenticate_required
