import httpx
from typing import Dict, Any, Optional
from urllib.parse import urlencode
from .base_provider import BaseAuthProvider, ExternalUserInfo

class GitHubAuthProvider(BaseAuthProvider):
    """GitHub OAuth authentication provider"""

    AUTHORIZATION_URL = "https://github.com/login/oauth/authorize"
    TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_INFO_URL = "https://api.github.com/user"
    USER_EMAILS_URL = "https://api.github.com/user/emails"
    SCOPE = "user:email"

    @property
    def provider_name(self) -> str:
        return "github"

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Get GitHub OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.SCOPE,
            "response_type": "code"
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
            "redirect_uri": self.redirect_uri
        }

        headers = {"Accept": "application/json"}

        async with httpx.AsyncClient() as client:
            response = await client.post(self.TOKEN_URL, data=data, headers=headers)
            response.raise_for_status()
            return response.json()

    async def get_user_info(self, access_token: str) -> ExternalUserInfo:
        """Get user information from GitHub"""
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/json"
        }

        async with httpx.AsyncClient() as client:
            # Get user info
            user_response = await client.get(self.USER_INFO_URL, headers=headers)
            user_response.raise_for_status()
            user_data = user_response.json()

            # Get user emails (GitHub may not return email in user info)
            email = user_data.get("email")
            if not email:
                emails_response = await client.get(self.USER_EMAILS_URL, headers=headers)
                if emails_response.status_code == 200:
                    emails = emails_response.json()
                    primary_email = next((e["email"] for e in emails if e["primary"]), None)
                    email = primary_email or (emails[0]["email"] if emails else None)

        # Parse name
        full_name = user_data.get("name", "").strip()
        name_parts = full_name.split(" ", 1) if full_name else ["", ""]
        first_name = name_parts[0] if len(name_parts) > 0 else None
        last_name = name_parts[1] if len(name_parts) > 1 else None

        return ExternalUserInfo(
            external_user_id=str(user_data["id"]),
            email=email,
            first_name=first_name,
            last_name=last_name,
            display_name=user_data.get("name") or user_data.get("login"),
            avatar_url=user_data.get("avatar_url"),
            provider="github",
            raw_data=user_data
        )
