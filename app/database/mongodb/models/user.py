from datetime import datetime
from typing import Optional, List
from pydantic import EmailStr, Field
from app.database.mongodb.models.base_model import MongoDBBaseModel, PyObjectId

class UserModel(MongoDBBaseModel):
    """MongoDB User model"""
    email: EmailStr = Field(..., unique=True, index=True)
    username: Optional[str] = Field(None, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    password_hash: Optional[str] = Field(None)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    tenant_id: Optional[str] = Field(default="default")
    roles: List[str] = Field(default=[])
    failed_login_attempts: int = Field(default=0)
    locked_until: Optional[datetime] = Field(None)
    
    class Config:
        collection_name = "users"
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": True,
                "tenant_id": "default",
                "roles": ["user"]
            }
        }
