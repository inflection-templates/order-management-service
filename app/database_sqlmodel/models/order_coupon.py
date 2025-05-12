# import json
# import uuid
# from sqlalchemy import Column, ForeignKey, String, Float, Boolean, DateTime, func
# from app.common.utils import generate_uuid4
# from app.database.base import Base

# class OrderCoupon(Base):

#     __tablename__ = "order_coupons"

#     id                 = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
#     Code               = Column(String(64))
#     CouponId           = Column(String(36), ForeignKey("coupons.id"))
#     OrderId            = Column(String(36), ForeignKey("orders.id"))
#     DiscountValue      = Column(Float, default=0.00)
#     DiscountPercentage = Column(Float, default=0.00)
#     DiscountMaxAmount  = Column(Float, default=0.00)
#     Applied            = Column(Boolean, default=True)
#     AppliedAt          = Column(DateTime(timezone=True), default=None)
#     CreatedAt          = Column(DateTime(timezone=True), server_default=func.now())
#     UpdatedAt          = Column(DateTime(timezone=True), onupdate=func.now())

#     def __init__(self, id, Code, OrderId,
#                  DiscountValue = 0.0, DiscountPercentage = 0.0,
#                  DiscountMaxAmount = 0.0, ExpiryDate = None,
#                  IsActive = True):
#         super().__init__()
#         self.id                 = id
#         self.Code               = Code
#         self.OrderId            = OrderId
#         self.DiscountValue      = DiscountValue
#         self.DiscountPercentage = DiscountPercentage
#         self.DiscountMaxAmount  = DiscountMaxAmount
#         self.ExpiryDate         = ExpiryDate
#         self.IsActive           = IsActive

#     def __repr__(self):
#         jsonStr = json.dumps(self.__dict__)
#         return jsonStr



from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.common.utils import generate_uuid4
from app.database.models.coupon import Coupon
from app.database.models.order import Order


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
    UpdatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow, on_update=datetime.utcnow)

    # Relationship to Coupon model and Order model
    coupon: Optional["Coupon"] = Relationship(back_populates="order_coupons")
    order: Optional["Order"] = Relationship(back_populates="order_coupons")

    def __repr__(self):
        return self.json(indent=2)
