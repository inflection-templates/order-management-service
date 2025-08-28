from typing import Optional, List
from pydantic import EmailStr, Field
from app.database.mongodb.models.base_model import MongoDBBaseModel

class CustomerModel(MongoDBBaseModel):
    """MongoDB Customer model"""
    email: EmailStr = Field(..., unique=True, index=True)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: bool = Field(default=True)
    tenant_id: Optional[str] = Field(default="default")
