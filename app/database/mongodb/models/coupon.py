from datetime import datetime
from typing import Optional
from pydantic import Field
from app.database.mongodb.models.base_model import MongoDBBaseModel

class CouponModel(MongoDBBaseModel):
    """MongoDB Coupon model"""
    Code: str = Field(..., unique=True, max_length=20)
    Description: Optional[str] = Field(None, max_length=200)
    DiscountPercentage: float = Field(..., ge=0.0, le=100.0)
    DiscountAmount: float = Field(..., ge=0.0)
    MinimumOrderAmount: float = Field(default=0.0, ge=0.0)
    MaximumDiscountAmount: Optional[float] = Field(None, ge=0.0)
    IsActive: bool = Field(default=True)
    ValidFrom: Optional[datetime] = Field(None)
    ValidTo: Optional[datetime] = Field(None)