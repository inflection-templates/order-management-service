from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

@dataclass
class ExternalUserInfo:
    """External user information from OAuth providers"""
    external_user_id: str
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: Optional[str]
    avatar_url: Optional[str]
    provider: str
    raw_data: Dict[str, Any]

class BaseAuthProvider(ABC):
    """Base class for external authentication providers"""

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name"""
        pass

    @abstractmethod
    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Get the authorization URL for OAuth flow"""
        pass

    @abstractmethod
    async def exchange_code_for_token(self, code: str, state: Optional[str] = None) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        pass

    @abstractmethod
    async def get_user_info(self, access_token: str) -> ExternalUserInfo:
        """Get user information using access token"""
        pass

    def is_enabled(self) -> bool:
        """Check if the provider is properly configured"""
        return bool(self.client_id and self.client_secret)
