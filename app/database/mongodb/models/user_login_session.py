from typing import Optional
from pydantic import BaseModel, Field
from app.database.mongodb.models.base_model import MongoDBBaseModel
from datetime import datetime, date

class UserLoginSessionModel(MongoDBBaseModel):
    """MongoDB model for user login sessions"""
    
    user_id: str = Field(..., description="User ID")
    is_active: bool = Field(default=True, description="Whether the session is active")
    started_at: Optional[date] = Field(None, description="Session start date")
    valid_till: date = Field(..., description="Session expiration date")
    deleted_at: Optional[datetime] = Field(None, description="Soft delete timestamp")