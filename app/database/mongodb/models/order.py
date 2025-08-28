from typing import Optional, List
from pydantic import Field
from app.database.mongodb.models.base_model import MongoDBBaseModel
from app.domain_types.enums.order_status_types import OrderStatusTypes

class OrderModel(MongoDBBaseModel):
    """MongoDB Order model"""
    DisplayCode: Optional[str] = Field(None, max_length=64)
    InvoiceNumber: Optional[str] = Field(None)
    OrderType: Optional[str] = Field(None, max_length=64)
    CustomerId: str = Field(...)
    AssociatedCartId: Optional[str] = Field(None)
    TotalItemsCount: int = Field(default=0, ge=0, le=100)
    OrderDiscount: float = Field(default=0.0, ge=0.0)
    TipApplicable: bool = Field(default=False)
    TipAmount: float = Field(default=0.0, ge=0.0)
    TotalTax: float = Field(default=0.0, ge=0.0)
    TotalDiscount: float = Field(default=0.0, ge=0.0)
    TotalAmount: float = Field(default=0.0, ge=0.0)
    Notes: Optional[str] = Field(None, max_length=1024)
    Coupons: Optional[List[str]] = Field(default=[])
    OrderStatus: OrderStatusTypes = Field(default=OrderStatusTypes.DRAFT)

