from typing import Optional
from pydantic import Field
from app.database.mongodb.models.base_model import MongoDBBaseModel

class OrderTypeModel(MongoDBBaseModel):
    """MongoDB Order Type model"""
    Name: str = Field(..., max_length=100)
    Description: Optional[str] = Field(None, max_length=500)
    IsActive: bool = Field(default=True)
    ProcessingTime: Optional[int] = Field(None, ge=0)  # in minutes
    DeliveryFee: float = Field(default=0.0, ge=0.0)