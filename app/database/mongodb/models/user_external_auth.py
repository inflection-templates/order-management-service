from typing import Optional
from pydantic import BaseModel, Field
from app.database.mongodb.models.base_model import MongoDBBaseModel
from datetime import datetime

class UserExternalAuthModel(MongoDBBaseModel):
    """MongoDB model for user external authentication"""
    
    user_id: str = Field(..., description="User ID")
    provider: str = Field(..., description="Authentication provider (google, facebook, github, twitter, gitlab, cognito, azure_ad, saml)")
    external_user_id: str = Field(..., description="External provider user ID")
    email: Optional[str] = Field(None, description="User email from external provider")
    display_name: Optional[str] = Field(None, description="User display name from external provider")
    access_token: Optional[str] = Field(None, description="OAuth access token")
    refresh_token: Optional[str] = Field(None, description="OAuth refresh token")
    token_expires_at: Optional[datetime] = Field(None, description="Token expiration timestamp")
    additional_data: Optional[dict] = Field(default_factory=dict, description="Provider-specific additional data")