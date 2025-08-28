from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.database.mongodb.models.base_model import MongoDBBaseModel, PyObjectId

class AuthTokenModel(MongoDBBaseModel):
    """MongoDB model for authentication tokens"""
    
    user_id: str = Field(..., description="User ID this token belongs to")
    token_type: str = Field(..., description="Type of token (access, refresh, reset_password, verify_email, invitation)")
    token: str = Field(..., description="The actual token value")
    is_revoked: bool = Field(default=False, description="Whether the token is revoked")
    expires_at: datetime = Field(..., description="Token expiration timestamp")
