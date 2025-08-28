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