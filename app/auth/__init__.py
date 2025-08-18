# Convenience imports for authentication
from .authenticate_decorator import authenticate_user
from .decorators import AuthContext, get_current_user, get_current_user_optional
from .auth_service import AuthService
from .jwt_service import JWTService

# New restructured JWT services (available for direct use if needed)
from .jwt_handler import JWTHandler
from .jwt_token_service import JWTTokenService
from .token_manager import TokenManager

__all__ = [
    'authenticate_user',
    'AuthContext',
    'get_current_user',
    'get_current_user_optional',
    'AuthService',
    'JWTService',
    # New services
    'JWTHandler',
    'JWTTokenService',
    'TokenManager'
]
