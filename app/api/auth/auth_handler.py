from typing import Dict, Any, Optional
# from  import Session
from fastapi import HTTPException, status, Request
from requests import Session

from app.auth.auth_service import AuthService
from app.auth.jwt_service import JWTService
from app.auth.user_flows import UserFlowService
from app.auth.sms_service import SMSService
from app.auth.email_service import EmailService
from app.domain_types.schemas.auth import (
    EmailPasswordLoginModel, PhonePasswordLoginModel, PhoneOTPLoginModel,
    TokenResponseModel, RefreshTokenModel, UserRegistrationModel,
    PasswordResetRequestModel, PasswordResetModel, ChangePasswordModel,
    TwoFactorSetupResponseModel, TwoFactorVerificationModel, SendOTPModel,
    UserProfileModel, UserInvitationModel, AcceptInvitationModel,
    EmailVerificationModel, PhoneVerificationModel
)
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.database_alchemy.models.user import User
from app.database_alchemy.models.tenant import Tenant
from app.telemetry.tracing import trace_span
from app.auth.decorators import AuthContext
import logging

logger = logging.getLogger(__name__)

class AuthHandler:

    @staticmethod
    @trace_span("handler: login_with_email_password")
    def login_with_email_password(
        model: EmailPasswordLoginModel,
        db_session: Session,
        request: Request
    ) -> ResponseModel[TokenResponseModel]:
        """Login with email and password"""
        try:
            user, error = AuthService.authenticate_with_email_password(
                db_session, model.email, model.password, model.tenant_id
            )

            if error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=error
                )

            # Check if 2FA is enabled
            if user.IsTwoFactorEnabled:
                # Create temporary token for 2FA verification
                temp_token = JWTService.create_special_token(
                    user_id=user.id,
                    tenant_id=user.TenantId,
                    token_type="temp_2fa",
                    session=db_session,
                    expires_hours=1,
                    additional_claims={"step": "2fa_required"}
                )

                return ResponseModel[TokenResponseModel](
                    Message="Two-factor authentication required",
                    Data=TokenResponseModel(
                        access_token=temp_token,
                        refresh_token="",
                        requires_2fa=True
                    )
                )

            # Create tokens
            tokens = AuthService.create_user_tokens(db_session, user)

            return ResponseModel[TokenResponseModel](
                Message="Login successful",
                Data=TokenResponseModel(**tokens)
            )

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: login_with_phone_password")
    def login_with_phone_password(
        model: PhonePasswordLoginModel,
        db_session: Session,
        request: Request
    ) -> ResponseModel[TokenResponseModel]:
        """Login with phone and password"""
        try:
            user, error = AuthService.authenticate_with_phone_password(
                db_session, model.phone, model.password, model.tenant_id
            )

            if error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=error
                )

            # Check if 2FA is enabled
            if user.IsTwoFactorEnabled:
                temp_token = JWTService.create_special_token(
                    user_id=user.id,
                    tenant_id=user.TenantId,
                    token_type="temp_2fa",
                    session=db_session,
                    expires_hours=1,
                    additional_claims={"step": "2fa_required"}
                )

                return ResponseModel[TokenResponseModel](
                    Message="Two-factor authentication required",
                    Data=TokenResponseModel(
                        access_token=temp_token,
                        refresh_token="",
                        requires_2fa=True
                    )
                )

            tokens = AuthService.create_user_tokens(db_session, user)

            return ResponseModel[TokenResponseModel](
                Message="Login successful",
                Data=TokenResponseModel(**tokens)
            )

        except Exception as e:
            logger.error(f"Phone login error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: send_otp")
    def send_otp(
        model: SendOTPModel,
        db_session: Session,
        request: Request
    ) -> ResponseModel[Dict[str, str]]:
        """Send OTP to phone or email"""
        try:
            # Find user by phone or email
            user = None
            if model.phone:
                user = db_session.query(User).filter(User.Phone == model.phone).first()
            elif model.email:
                user = db_session.query(User).filter(User.Email == model.email).first()

            if not user:
                # For security, don't reveal if user exists
                return ResponseModel[Dict[str, str]](
                    Message="If the phone/email exists, OTP has been sent",
                    Data={"status": "sent"}
                )

            # Generate and send OTP
            otp_code = AuthService.generate_otp(
                db_session, user.id, model.purpose, model.phone, model.email
            )

            # Send actual SMS/Email
            if model.phone:
                SMSService.send_otp_sms(model.phone, otp_code, model.purpose)
                logger.info(f"OTP sent via SMS to {model.phone}")
            elif model.email:
                EmailService.send_otp_email(model.email, otp_code, model.purpose)
                logger.info(f"OTP sent via email to {model.email}")

            return ResponseModel[Dict[str, str]](
                Message="OTP sent successfully",
                Data={"status": "sent"}
            )

        except Exception as e:
            logger.error(f"Send OTP error: {str(e)}")
            db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send OTP"
            )
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: login_with_phone_otp")
    def login_with_phone_otp(
        model: PhoneOTPLoginModel,
        db_session: Session,
        request: Request
    ) -> ResponseModel[TokenResponseModel]:
        """Login with phone and OTP"""
        try:
            user, error = AuthService.authenticate_with_phone_otp(
                db_session, model.phone, model.otp_code, model.tenant_id
            )

            if error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=error
                )

            tokens = AuthService.create_user_tokens(db_session, user)

            return ResponseModel[TokenResponseModel](
                Message="Login successful",
                Data=TokenResponseModel(**tokens)
            )

        except Exception as e:
            logger.error(f"OTP login error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: setup_two_factor")
    def setup_two_factor(
        db_session: Session,
        request: Request,
        auth_context: AuthContext
    ) -> ResponseModel[TwoFactorSetupResponseModel]:
        """Setup two-factor authentication"""
        try:
            setup_data = AuthService.setup_two_factor(db_session, auth_context.user_id)

            return ResponseModel[TwoFactorSetupResponseModel](
                Message="Two-factor authentication setup initiated",
                Data=TwoFactorSetupResponseModel(**setup_data)
            )

        except Exception as e:
            logger.error(f"2FA setup error: {str(e)}")
            db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to setup two-factor authentication"
            )
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: verify_two_factor_setup")
    def verify_two_factor_setup(
        model: TwoFactorVerificationModel,
        db_session: Session,
        request: Request,
        auth_context: AuthContext
    ) -> ResponseModel[Dict[str, bool]]:
        """Verify two-factor authentication setup"""
        try:
            success = AuthService.verify_two_factor_setup(
                db_session, auth_context.user_id, model.totp_code
            )

            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid TOTP code"
                )

            return ResponseModel[Dict[str, bool]](
                Message="Two-factor authentication enabled successfully",
                Data={"enabled": True}
            )

        except Exception as e:
            logger.error(f"2FA verification error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: refresh_token")
    def refresh_token(
        model: RefreshTokenModel,
        db_session: Session,
        request: Request
    ) -> ResponseModel[TokenResponseModel]:
        """Refresh access token"""
        try:
            tokens = AuthService.refresh_access_token(db_session, model.refresh_token)

            if not tokens:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired refresh token"
                )

            return ResponseModel[TokenResponseModel](
                Message="Token refreshed successfully",
                Data=TokenResponseModel(**tokens)
            )

        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: logout")
    def logout(
        db_session: Session,
        request: Request,
        auth_context: AuthContext
    ) -> ResponseModel[Dict[str, str]]:
        """Logout user"""
        try:
            # Revoke all user tokens
            JWTService.revoke_all_user_tokens(auth_context.user_id, db_session)

            return ResponseModel[Dict[str, str]](
                Message="Logout successful",
                Data={"status": "logged_out"}
            )

        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Logout failed"
            )
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: get_profile")
    def get_profile(
        db_session: Session,
        request: Request,
        auth_context: AuthContext
    ) -> ResponseModel[UserProfileModel]:
        """Get user profile"""
        try:
            user = auth_context.user

            profile = UserProfileModel(
                id=user.id,
                tenant_id=user.TenantId,
                first_name=user.FirstName,
                last_name=user.LastName,
                email=user.Email,
                phone=user.Phone,
                is_email_verified=user.IsEmailVerified,
                is_phone_verified=user.IsPhoneVerified,
                is_two_factor_enabled=user.IsTwoFactorEnabled,
                last_login_at=user.LastLoginAt,
                created_at=user.CreatedAt
            )

            return ResponseModel[UserProfileModel](
                Message="Profile retrieved successfully",
                Data=profile
            )

        except Exception as e:
            logger.error(f"Get profile error: {str(e)}")
            db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve profile"
            )
        finally:
            db_session.close()

    # User Flow Methods

    @staticmethod
    @trace_span("handler: send_invitation")
    def send_invitation(
        model: UserInvitationModel,
        db_session: Session,
        request: Request,
        auth_context: AuthContext
    ) -> ResponseModel[Dict[str, str]]:
        """Send user invitation"""
        try:
            token = UserFlowService.send_invitation_email(
                session=db_session,
                email=model.email,
                first_name=model.first_name,
                last_name=model.last_name,
                role_ids=model.role_ids,
                tenant_id=model.tenant_id or auth_context.tenant_id,
                message=model.message,
                invited_by_user_id=auth_context.user_id
            )

            return ResponseModel[Dict[str, str]](
                Message="Invitation sent successfully",
                Data={"invitation_token": token}
            )

        except Exception as e:
            logger.error(f"Send invitation error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: accept_invitation")
    def accept_invitation(
        model: AcceptInvitationModel,
        db_session: Session,
        request: Request
    ) -> ResponseModel[TokenResponseModel]:
        """Accept user invitation"""
        try:
            user = UserFlowService.accept_invitation(
                db_session, model.token, model.password, model.first_name, model.last_name
            )

            # Send welcome email
            UserFlowService.send_welcome_email(db_session, user.id)

            # Create tokens
            tokens = AuthService.create_user_tokens(db_session, user)

            return ResponseModel[TokenResponseModel](
                Message="Invitation accepted successfully",
                Data=TokenResponseModel(**tokens)
            )

        except Exception as e:
            logger.error(f"Accept invitation error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: request_password_reset")
    def request_password_reset(
        model: PasswordResetRequestModel,
        db_session: Session,
        request: Request
    ) -> ResponseModel[Dict[str, str]]:
        """Request password reset"""
        try:
            token = UserFlowService.request_password_reset(
                db_session, model.email, model.phone, model.tenant_id
            )

            return ResponseModel[Dict[str, str]](
                Message="If the email/phone exists, password reset instructions have been sent",
                Data={"status": "sent"}
            )

        except Exception as e:
            logger.error(f"Password reset request error: {str(e)}")
            db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process password reset request"
            )
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: reset_password")
    def reset_password(
        model: PasswordResetModel,
        db_session: Session,
        request: Request
    ) -> ResponseModel[Dict[str, bool]]:
        """Reset password using token"""
        try:
            success = UserFlowService.reset_password(
                db_session, model.token, model.new_password
            )

            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired reset token"
                )

            return ResponseModel[Dict[str, bool]](
                Message="Password reset successfully",
                Data={"success": True}
            )

        except Exception as e:
            logger.error(f"Reset password error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: change_password")
    def change_password(
        model: ChangePasswordModel,
        db_session: Session,
        request: Request,
        auth_context: AuthContext
    ) -> ResponseModel[Dict[str, bool]]:
        """Change user password"""
        try:
            success = UserFlowService.change_password(
                db_session, auth_context.user_id, model.current_password, model.new_password
            )

            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid current password"
                )

            return ResponseModel[Dict[str, bool]](
                Message="Password changed successfully",
                Data={"success": True}
            )

        except Exception as e:
            logger.error(f"Change password error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: verify_email")
    def verify_email(
        model: EmailVerificationModel,
        db_session: Session,
        request: Request
    ) -> ResponseModel[Dict[str, bool]]:
        """Verify email using token"""
        try:
            success = UserFlowService.verify_email(db_session, model.token)

            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired verification token"
                )

            return ResponseModel[Dict[str, bool]](
                Message="Email verified successfully",
                Data={"verified": True}
            )

        except Exception as e:
            logger.error(f"Email verification error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: send_phone_verification")
    def send_phone_verification(
        db_session: Session,
        request: Request,
        auth_context: AuthContext
    ) -> ResponseModel[Dict[str, str]]:
        """Send phone verification OTP"""
        try:
            UserFlowService.send_phone_verification_otp(db_session, auth_context.user_id)

            return ResponseModel[Dict[str, str]](
                Message="Verification OTP sent to phone",
                Data={"status": "sent"}
            )

        except Exception as e:
            logger.error(f"Send phone verification error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: verify_phone")
    def verify_phone(
        model: PhoneVerificationModel,
        db_session: Session,
        request: Request,
        auth_context: AuthContext
    ) -> ResponseModel[Dict[str, bool]]:
        """Verify phone using OTP"""
        try:
            success = UserFlowService.verify_phone(
                db_session, auth_context.user_id, model.otp_code
            )

            if not success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired OTP"
                )

            return ResponseModel[Dict[str, bool]](
                Message="Phone verified successfully",
                Data={"verified": True}
            )

        except Exception as e:
            logger.error(f"Phone verification error: {str(e)}")
            db_session.rollback()
            raise e
        finally:
            db_session.close()
