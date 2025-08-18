from typing import Dict, Type, Optional
from app.config.config import get_settings
from .base_provider import BaseAuthProvider
from .google_provider import GoogleAuthProvider
from .github_provider import GitHubAuthProvider

settings = get_settings()

class ProviderFactory:
    """Factory for creating authentication providers"""

    _providers: Dict[str, Type[BaseAuthProvider]] = {
        "google": GoogleAuthProvider,
        "github": GitHubAuthProvider,
    }

    @classmethod
    def register_provider(cls, name: str, provider_class: Type[BaseAuthProvider]):
        """Register a new authentication provider"""
        cls._providers[name] = provider_class

    @classmethod
    def create_provider(cls, provider_name: str, redirect_uri: str) -> Optional[BaseAuthProvider]:
        """Create an authentication provider instance"""
        if provider_name not in cls._providers:
            return None

        provider_class = cls._providers[provider_name]

        # Get provider-specific configuration
        client_id = None
        client_secret = None

        if provider_name == "google":
            client_id = settings.GOOGLE_CLIENT_ID
            client_secret = settings.GOOGLE_CLIENT_SECRET
        elif provider_name == "github":
            client_id = settings.GITHUB_CLIENT_ID
            client_secret = settings.GITHUB_CLIENT_SECRET
        elif provider_name == "facebook":
            client_id = settings.FACEBOOK_CLIENT_ID
            client_secret = settings.FACEBOOK_CLIENT_SECRET
        elif provider_name == "twitter":
            client_id = settings.TWITTER_CLIENT_ID
            client_secret = settings.TWITTER_CLIENT_SECRET
        elif provider_name == "gitlab":
            client_id = settings.GITLAB_CLIENT_ID
            client_secret = settings.GITLAB_CLIENT_SECRET

        if not client_id or not client_secret:
            return None

        return provider_class(client_id, client_secret, redirect_uri)

    @classmethod
    def get_available_providers(cls) -> list[str]:
        """Get list of available and configured providers"""
        available = []

        if settings.ENABLE_SOCIAL_LOGIN:
            for provider_name in cls._providers.keys():
                provider = cls.create_provider(provider_name, "dummy")
                if provider and provider.is_enabled():
                    available.append(provider_name)

        return available

    @classmethod
    def is_provider_enabled(cls, provider_name: str) -> bool:
        """Check if a provider is enabled and configured"""
        if not settings.ENABLE_SOCIAL_LOGIN:
            return False

        provider = cls.create_provider(provider_name, "dummy")
        return provider is not None and provider.is_enabled()
