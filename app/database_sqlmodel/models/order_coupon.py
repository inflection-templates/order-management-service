from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.common.utils import generate_uuid4
from app.database_sqlmodel.models.coupon import Coupon
from app.database_sqlmodel.models.order import Order

class OrderCoupon(SQLModel, table=True):
    __tablename__ = "order_coupons"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    Code: str = Field(default=None, max_length=64)
    CouponId: Optional[str] = Field(default=None, foreign_key="coupons.id", max_length=36)
    OrderId: Optional[str] = Field(default=None, foreign_key="orders.id", max_length=36)
    DiscountValue: float = Field(default=0.00)
    DiscountPercentage: float = Field(default=0.00)
    DiscountMaxAmount: float = Field(default=0.00)
    Applied: bool = Field(default=True)
    AppliedAt: Optional[datetime] = Field(default=None, nullable=True)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow)

    coupon: Optional["Coupon"] = Relationship(back_populates="order_coupons")
    order: Optional["Order"] = Relationship(back_populates="order_coupons")

    def __repr__(self):
        return self.json(indent=2)
