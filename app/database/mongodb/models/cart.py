from typing import Optional, List
from pydantic import Field
from app.database.mongodb.models.base_model import MongoDBBaseModel

class CartModel(MongoDBBaseModel):
    """MongoDB Cart model"""
    CustomerId: str = Field(...)
    IsActive: bool = Field(default=True)
    TotalItemsCount: int = Field(default=0, ge=0)
    TotalAmount: float = Field(default=0.0, ge=0.0)
    Notes: Optional[str] = Field(None, max_length=500)
