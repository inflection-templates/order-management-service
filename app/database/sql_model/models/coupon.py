from sqlmodel import SQLModel, Field, Enum
from typing import Optional
from datetime import datetime
from app.common.utils import generate_uuid4
from app.domain_types.enums.discount_type import DiscountTypes

class Coupon(SQLModel, table=True):
    __tablename__ = "coupons"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    Name: str = Field(max_length=64)
    Description: str = Field(max_length=1024)
    CouponCode: str = Field(unique=True, max_length=64)
    CouponType: Optional[str] = Field(default=None, max_length=64)
    Discount: float = Field(default=0.00)
    DiscountType: DiscountTypes = Field(default=DiscountTypes.FLAT)
    DiscountPercentage: float = Field(default=0.00)
    DiscountMaxAmount: float = Field(default=0.00)
    StartDate: Optional[datetime] = None
    EndDate: Optional[datetime] = None
    MaxUsage: int = Field(default=10000)
    MaxUsagePerUser: int = Field(default=1)
    MaxUsagePerOrder: int = Field(default=1)
    MinOrderAmount: float = Field(default=0.00)
    IsActive: bool = Field(default=True)
    IsDeleted: bool = Field(default=False)
    CreatedBy: Optional[str] = Field(default=None, max_length=36)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: Optional[datetime] = None

    def __repr__(self):
        return self.json(indent=2)
