from typing import Optional
from pydantic import BaseModel, Field
from app.database.mongodb.models.base_model import MongoDBBaseModel
from datetime import datetime

class UserRoleModel(MongoDBBaseModel):
    """MongoDB model for user-role relationships"""
    
    user_id: str = Field(..., description="User ID")
    role_id: int = Field(..., description="Role ID")
    deleted_at: Optional[datetime] = Field(None, description="Soft delete timestamp")