from typing import Optional, List
from pydantic import Field
from app.database.mongodb.models.base_model import MongoDBBaseModel

class ApiClientModel(MongoDBBaseModel):
    """MongoDB API Client model"""
    Name: str = Field(..., max_length=100)
    Description: Optional[str] = Field(None, max_length=500)
    ClientId: str = Field(..., unique=True, max_length=100)
    ClientSecret: str = Field(..., max_length=200)
    Scopes: List[str] = Field(default=[])
    IsActive: bool = Field(default=True)
    RateLimit: Optional[int] = Field(None, ge=0)  # requests per minute
    
    class Config:
        collection_name = "api_clients"
        schema_extra = {
            "example": {
                "Name": "Mobile App Client",
                "Description": "API client for mobile application",
                "ClientId": "mobile_app_123",
                "ClientSecret": "secret_key_here",
                "Scopes": ["read", "write"],
                "IsActive": True,
                "RateLimit": 1000
            }
        }