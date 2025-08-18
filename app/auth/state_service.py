import secrets
from typing import Optional
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

class StateService:
    """Service for managing OAuth state parameters for CSRF protection"""

    # In-memory storage for development (use Redis in production)
    _state_store = {}

    @staticmethod
    def generate_state(tenant_id: str = None, additional_data: dict = None) -> str:
        """Generate OAuth state parameter with optional data"""
        state = secrets.token_urlsafe(32)

        state_data = {
            "tenant_id": tenant_id,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(minutes=10)).isoformat(),
            "additional_data": additional_data or {}
        }

        # Store state (in production, use Redis with expiration)
        StateService._state_store[state] = state_data

        logger.info(f"Generated OAuth state: {state}")
        return state

    @staticmethod
    def verify_state(state: str) -> Optional[dict]:
        """Verify OAuth state parameter and return stored data"""
        if not state:
            logger.warning("No state parameter provided")
            return None

        state_data = StateService._state_store.get(state)
        if not state_data:
            logger.warning(f"Invalid state parameter: {state}")
            return None

        # Check expiration
        expires_at = datetime.fromisoformat(state_data["expires_at"])
        if datetime.utcnow() > expires_at:
            logger.warning(f"Expired state parameter: {state}")
            # Clean up expired state
            StateService._state_store.pop(state, None)
            return None

        # Remove from store (one-time use)
        StateService._state_store.pop(state, None)

        logger.info(f"Verified OAuth state: {state}")
        return state_data

    @staticmethod
    def cleanup_expired_states():
        """Clean up expired state parameters (call periodically)"""
        now = datetime.utcnow()
        expired_states = []

        for state, data in StateService._state_store.items():
            expires_at = datetime.fromisoformat(data["expires_at"])
            if now > expires_at:
                expired_states.append(state)

        for state in expired_states:
            StateService._state_store.pop(state, None)

        if expired_states:
            logger.info(f"Cleaned up {len(expired_states)} expired OAuth states")

# Production Redis implementation (uncomment and use in production)
"""
import redis
from app.config.config import get_settings

settings = get_settings()

class RedisStateService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    def generate_state(self, tenant_id: str = None, additional_data: dict = None) -> str:
        state = secrets.token_urlsafe(32)

        state_data = {
            "tenant_id": tenant_id,
            "created_at": datetime.utcnow().isoformat(),
            "additional_data": additional_data or {}
        }

        # Store with 10 minute expiration
        self.redis_client.setex(
            f"oauth_state:{state}",
            600,  # 10 minutes
            json.dumps(state_data)
        )

        return state

    def verify_state(self, state: str) -> Optional[dict]:
        if not state:
            return None

        state_data_json = self.redis_client.get(f"oauth_state:{state}")
        if not state_data_json:
            return None

        # Remove from Redis (one-time use)
        self.redis_client.delete(f"oauth_state:{state}")

        return json.loads(state_data_json)
"""
