from typing import Optional
from pydantic import Field
from app.database.mongodb.models.base_model import MongoDBBaseModel

class OrderLineItemModel(MongoDBBaseModel):
    """MongoDB Order Line Item model"""
    OrderId: str = Field(...)
    ProductId: str = Field(...)
    ProductName: str = Field(..., max_length=200)
    Quantity: int = Field(..., ge=1)
    UnitPrice: float = Field(..., ge=0.0)
    TotalPrice: float = Field(..., ge=0.0)
    Notes: Optional[str] = Field(None, max_length=500)