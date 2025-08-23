from typing import Optional
from pydantic import Field
from app.database.mongodb.models.base_model import MongoDBBaseModel

class MerchantModel(MongoDBBaseModel):
    """MongoDB Merchant model"""
    Name: str = Field(..., max_length=100)
    Description: Optional[str] = Field(None, max_length=500)
    IsActive: bool = Field(default=True)
    ContactEmail: Optional[str] = Field(None, max_length=100)
    ContactPhone: Optional[str] = Field(None, max_length=20)
    
    class Config:
        collection_name = "merchants"
        schema_extra = {
            "example": {
                "Name": "Sample Merchant",
                "Description": "A sample merchant for testing",
                "IsActive": True
            }
        }
