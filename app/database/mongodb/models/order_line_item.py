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
    
    class Config:
        collection_name = "order_line_items"
        schema_extra = {
            "example": {
                "OrderId": "order123",
                "ProductId": "product456",
                "ProductName": "Sample Product",
                "Quantity": 2,
                "UnitPrice": 29.99,
                "TotalPrice": 59.98
            }
        }