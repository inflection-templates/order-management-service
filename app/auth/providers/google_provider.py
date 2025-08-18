import httpx
from typing import Dict, Any, Optional
from urllib.parse import urlencode
from .base_provider import BaseAuthProvider, ExternalUserInfo

class GoogleAuthProvider(BaseAuthProvider):
    """Google OAuth 2.0 authentication provider"""

    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    SCOPE = "openid email profile"

    @property
    def provider_name(self) -> str:
        return "google"

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Get Google OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.SCOPE,
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent"
        }

        if state:
            params["state"] = state

        return f"{self.AUTHORIZATION_URL}?{urlencode(params)}"

    async def exchange_code_for_token(self, code: str, state: Optional[str] = None) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.TOKEN_URL, data=data)
            response.raise_for_status()
            return response.json()

    async def get_user_info(self, access_token: str) -> ExternalUserInfo:
        """Get user information from Google"""
        headers = {"Authorization": f"Bearer {access_token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(self.USER_INFO_URL, headers=headers)
            response.raise_for_status()
            user_data = response.json()

        return ExternalUserInfo(
            external_user_id=user_data["id"],
            email=user_data.get("email"),
            first_name=user_data.get("given_name"),
            last_name=user_data.get("family_name"),
            display_name=user_data.get("name"),
            avatar_url=user_data.get("picture"),
            provider="google",
            raw_data=user_data
        )
