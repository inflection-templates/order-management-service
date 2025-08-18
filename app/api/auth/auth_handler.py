from datetime import timedelta
from sqlalchemy.orm import Session
from app.domain_types.schemas.auth import LoginModel, LoginResponseModel, TokenData
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.common.auth_utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database.services.users_service import get_user_by_email, verify_password
from app.common.error_utils import handle_service_exception, safe_execute_service_operation
from app.domain_types.miscellaneous.exceptions import Unauthorized, NotFound

def authenticate_user(session: Session, email: str, password: str, role: str):
    """Authenticate user with email, password and role"""
    # Check if user exists
    user = get_user_by_email(session, email)
    if not user:
        raise NotFound(f"User with email '{email}' not found")
    
    # Check password
    if not verify_password(password, user.Password):
        raise Unauthorized("Invalid password")
    
    return user

def login_(login_data: LoginModel, db_session: Session):
    """Handle user login and return JWT token"""
    try:
        def operation():
            user = authenticate_user(db_session, login_data.Email, login_data.Password, login_data.Role.value)
            
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token, expires_at = create_access_token(
                data={
                    "sub": user.id,
                    "email": user.Email, 
                    "role": login_data.Role.value
                },
                expires_delta=access_token_expires
            )
            
            return LoginResponseModel(
                access_token=access_token,
                token_type="bearer",
                user_id=user.id,
                email=user.Email,
                role=login_data.Role.value,
                expires_at=expires_at
            )
        
        login_response = safe_execute_service_operation(
            operation, 
            "user authentication", 
            db_session
        )
        
        message = "Login successful"
        resp = ResponseModel[LoginResponseModel](
            Message=message, Data=login_response, HttpCode=200)
        return resp
        
    except Exception as e:
        db_session.rollback()
        raise handle_service_exception(e, "user authentication")
    finally:
        db_session.close()


def get_current_user_info_(current_user: TokenData):
    """Get current authenticated user information"""
    try:
        def operation():
            return current_user
        
        user_info = safe_execute_service_operation(
            operation, 
            "user information retrieval"
        )
        
        message = "User information retrieved successfully"
        resp = ResponseModel[TokenData](
            Message=message, Data=user_info, HttpCode=200)
        return resp
        
    except Exception as e:
        raise handle_service_exception(e, "user information retrieval")


def logout_():
    """Handle user logout"""
    try:
        def operation():
            return {"message": "Successfully logged out"}
        
        logout_response = safe_execute_service_operation(
            operation, 
            "user logout"
        )
        
        message = "Logout successful"
        resp = ResponseModel[dict](
            Message=message, Data=logout_response, HttpCode=200)
        return resp
        
    except Exception as e:
        raise handle_service_exception(e, "user logout")
