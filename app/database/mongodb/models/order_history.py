from typing import Optional
from pydantic import Field
from app.database.mongodb.models.base_model import MongoDBBaseModel
from app.domain_types.enums.order_status_types import OrderStatusTypes

class OrderHistoryModel(MongoDBBaseModel):
    """MongoDB Order History model"""
    OrderId: str = Field(...)
    Status: OrderStatusTypes = Field(...)
    PreviousStatus: Optional[OrderStatusTypes] = Field(None)
    Notes: Optional[str] = Field(None, max_length=500)
    ChangedBy: Optional[str] = Field(None, max_length=100)
    
    class Config:
        collection_name = "order_history"
        schema_extra = {
            "example": {
                "OrderId": "order123",
                "Status": "CONFIRMED",
                "PreviousStatus": "PENDING",
                "Notes": "Order confirmed by customer",
                "ChangedBy": "system"
            }
        }
