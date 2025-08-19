from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.api.auth.auth_handler import AuthHandler
from app.api.auth.external_auth_handler import ExternalAuthHandler
from app.database_alchemy.database_accessor import get_db_session
from app.domain_types.schemas.auth import (
    EmailPasswordLoginModel, PhonePasswordLoginModel, PhoneOTPLoginModel,
    TokenResponseModel, RefreshTokenModel, UserRegistrationModel,
    PasswordResetRequestModel, PasswordResetModel, ChangePasswordModel,
    TwoFactorSetupResponseModel, TwoFactorVerificationModel, SendOTPModel,
    UserProfileModel, ExternalAuthURLModel, ExternalAuthCallbackModel,
    UserInvitationModel, AcceptInvitationModel, EmailVerificationModel,
    PhoneVerificationModel
)
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.auth import authenticate_user, AuthContext
from typing import Dict, Any

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

# Public endpoints (no authentication required)

@router.post("/login/email", status_code=status.HTTP_200_OK, response_model=ResponseModel[TokenResponseModel])
async def login_with_email_password(
    model: EmailPasswordLoginModel,
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Login with email and password"""
    return AuthHandler.login_with_email_password(model, db_session, request)

@router.post("/login/phone", status_code=status.HTTP_200_OK, response_model=ResponseModel[TokenResponseModel])
async def login_with_phone_password(
    model: PhonePasswordLoginModel,
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Login with phone and password"""
    return AuthHandler.login_with_phone_password(model, db_session, request)

@router.post("/login/phone-otp", status_code=status.HTTP_200_OK, response_model=ResponseModel[TokenResponseModel])
async def login_with_phone_otp(
    model: PhoneOTPLoginModel,
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Login with phone and OTP"""
    return AuthHandler.login_with_phone_otp(model, db_session, request)

@router.post("/otp/send", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, str]])
async def send_otp(
    model: SendOTPModel,
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Send OTP to phone or email"""
    return AuthHandler.send_otp(model, db_session, request)

@router.post("/token/refresh", status_code=status.HTTP_200_OK, response_model=ResponseModel[TokenResponseModel])
async def refresh_token(
    model: RefreshTokenModel,
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Refresh access token"""
    return AuthHandler.refresh_token(model, db_session, request)

# Protected endpoints (authentication required)

@router.post("/logout", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, str]])
@authenticate_user(required=True)
async def logout(
    request: Request,
    db_session: Session = Depends(get_db_session),
    **kwargs
):
    """Logout user and revoke tokens"""
    auth_context = kwargs.get('auth_context')
    return AuthHandler.logout(db_session, request, auth_context)

@router.get("/profile", status_code=status.HTTP_200_OK, response_model=ResponseModel[UserProfileModel])
@authenticate_user(required=True)
async def get_profile(
    request: Request,
    db_session: Session = Depends(get_db_session),
    **kwargs
):
    """Get current user profile"""
    auth_context = kwargs.get('auth_context')
    return AuthHandler.get_profile(db_session, request, auth_context)

@router.post("/2fa/setup", status_code=status.HTTP_200_OK, response_model=ResponseModel[TwoFactorSetupResponseModel])
@authenticate_user(required=True)
async def setup_two_factor(
    request: Request,
    db_session: Session = Depends(get_db_session),
    **kwargs
):
    """Setup two-factor authentication"""
    auth_context = kwargs.get('auth_context')
    return AuthHandler.setup_two_factor(db_session, request, auth_context)

@router.post("/2fa/verify", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, bool]])
@authenticate_user(required=True)
async def verify_two_factor_setup(
    model: TwoFactorVerificationModel,
    request: Request,
    db_session: Session = Depends(get_db_session),
    **kwargs
):
    """Verify and enable two-factor authentication"""
    auth_context = kwargs.get('auth_context')
    return AuthHandler.verify_two_factor_setup(model, db_session, request, auth_context)

# External Authentication endpoints

@router.get("/providers", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, Any]])
async def get_available_providers(
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Get available external authentication providers"""
    return ExternalAuthHandler.get_available_providers(db_session, request)

@router.post("/external/url", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, str]])
async def get_external_auth_url(
    model: ExternalAuthURLModel,
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Get external authentication URL"""
    return ExternalAuthHandler.get_external_auth_url(model, db_session, request)

@router.post("/external/callback", status_code=status.HTTP_200_OK, response_model=ResponseModel[TokenResponseModel])
async def external_auth_callback(
    model: ExternalAuthCallbackModel,
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Handle external authentication callback"""
    return await ExternalAuthHandler.external_auth_callback(model, db_session, request)

# User Flow endpoints

@router.post("/invite", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, str]])
@authenticate_user(required=True, roles=["admin", "manager"])
async def send_invitation(
    model: UserInvitationModel,
    request: Request,
    db_session: Session = Depends(get_db_session),
    **kwargs
):
    """Send user invitation (requires admin/manager role)"""
    auth_context = kwargs.get('auth_context')
    return AuthHandler.send_invitation(model, db_session, request, auth_context)

@router.post("/accept-invitation", status_code=status.HTTP_200_OK, response_model=ResponseModel[TokenResponseModel])
async def accept_invitation(
    model: AcceptInvitationModel,
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Accept user invitation"""
    return AuthHandler.accept_invitation(model, db_session, request)

@router.post("/password/reset-request", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, str]])
async def request_password_reset(
    model: PasswordResetRequestModel,
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Request password reset"""
    return AuthHandler.request_password_reset(model, db_session, request)

@router.post("/password/reset", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, bool]])
async def reset_password(
    model: PasswordResetModel,
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Reset password using token"""
    return AuthHandler.reset_password(model, db_session, request)

@router.post("/password/change", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, bool]])
@authenticate_user(required=True)
async def change_password(
    model: ChangePasswordModel,
    request: Request,
    db_session: Session = Depends(get_db_session),
    **kwargs
):
    """Change user password"""
    auth_context = kwargs.get('auth_context')
    return AuthHandler.change_password(model, db_session, request, auth_context)

@router.post("/verify/email", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, bool]])
async def verify_email(
    model: EmailVerificationModel,
    request: Request,
    db_session: Session = Depends(get_db_session)
):
    """Verify email using token"""
    return AuthHandler.verify_email(model, db_session, request)

@router.post("/verify/phone/send", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, str]])
@authenticate_user(required=True)
async def send_phone_verification(
    request: Request,
    db_session: Session = Depends(get_db_session),
    **kwargs
):
    """Send phone verification OTP"""
    auth_context = kwargs.get('auth_context')
    return AuthHandler.send_phone_verification(db_session, request, auth_context)

@router.post("/verify/phone", status_code=status.HTTP_200_OK, response_model=ResponseModel[Dict[str, bool]])
@authenticate_user(required=True)
async def verify_phone(
    model: PhoneVerificationModel,
    request: Request,
    db_session: Session = Depends(get_db_session),
    **kwargs
):
    """Verify phone using OTP"""
    auth_context = kwargs.get('auth_context')
    return AuthHandler.verify_phone(model, db_session, request, auth_context)
