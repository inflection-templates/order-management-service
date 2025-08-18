from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
import secrets
import logging

from app.auth.providers.provider_factory import ProviderFactory
from app.auth.auth_service import AuthService
from app.auth.state_service import StateService
from app.domain_types.schemas.auth import ExternalAuthURLModel, ExternalAuthCallbackModel, TokenResponseModel
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.telemetry.tracing import trace_span

logger = logging.getLogger(__name__)

class ExternalAuthHandler:

    @staticmethod
    @trace_span("handler: get_external_auth_url")
    def get_external_auth_url(
        model: ExternalAuthURLModel,
        db_session: Session,
        request: Request
    ) -> ResponseModel[Dict[str, str]]:
        """Get external authentication URL"""
        try:
            provider = ProviderFactory.create_provider(model.provider, model.redirect_uri)
            if not provider:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Provider {model.provider} not available or not configured"
                )

                        # Generate state for CSRF protection
            state = StateService.generate_state(
                tenant_id=model.tenant_id,
                additional_data={"provider": model.provider}
            )

            auth_url = provider.get_authorization_url(state)

            return ResponseModel[Dict[str, str]](
                Message="Authorization URL generated",
                Data={
                    "auth_url": auth_url,
                    "state": state,
                    "provider": model.provider
                }
            )

        except Exception as e:
            logger.error(f"External auth URL error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate authorization URL"
            )
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: external_auth_callback")
    async def external_auth_callback(
        model: ExternalAuthCallbackModel,
        db_session: Session,
        request: Request
    ) -> ResponseModel[TokenResponseModel]:
        """Handle external authentication callback"""
        try:
            # Construct redirect URI from request
            redirect_uri = f"{request.url.scheme}://{request.url.netloc}/auth/callback/{model.provider}"

            provider = ProviderFactory.create_provider(model.provider, redirect_uri)
            if not provider:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Provider {model.provider} not available"
                )

            # Verify state parameter for CSRF protection
            state_data = StateService.verify_state(model.state)
            if not state_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired state parameter"
                )
            
            # Verify provider matches
            if state_data.get("additional_data", {}).get("provider") != model.provider:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Provider mismatch in state parameter"
                )
            
            # Use tenant from state if not provided
            if not model.tenant_id:
                model.tenant_id = state_data.get("tenant_id")

            # Exchange code for access token
            token_data = await provider.exchange_code_for_token(model.code, model.state)
            access_token = token_data.get("access_token")

            if not access_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to obtain access token"
                )

            # Get user info from provider
            user_info = await provider.get_user_info(access_token)

            # Create or get existing user
            user = AuthService.create_external_auth_user(
                session=db_session,
                provider=model.provider,
                external_user_id=user_info.external_user_id,
                email=user_info.email,
                display_name=user_info.display_name,
                tenant_id=model.tenant_id,
                additional_data=user_info.raw_data
            )

            # Create JWT tokens
            tokens = AuthService.create_user_tokens(db_session, user)

            return ResponseModel[TokenResponseModel](
                Message="External authentication successful",
                Data=TokenResponseModel(**tokens)
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"External auth callback error: {str(e)}")
            db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="External authentication failed"
            )
        finally:
            db_session.close()

    @staticmethod
    @trace_span("handler: get_available_providers")
    def get_available_providers(
        db_session: Session,
        request: Request
    ) -> ResponseModel[Dict[str, Any]]:
        """Get list of available external authentication providers"""
        try:
            providers = ProviderFactory.get_available_providers()

            return ResponseModel[Dict[str, Any]](
                Message="Available providers retrieved",
                Data={"providers": providers}
            )

        except Exception as e:
            logger.error(f"Get providers error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve providers"
            )
        finally:
            db_session.close()
