import json
import uuid
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.database.connector import Base

class OrderCoupon(Base):
    __tablename__ = "coupons"
    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    Code = Column(String(64))
    CouponType = relationship("CouponType", back_populates="Coupons", default=None)
    DiscountValue = Column(Float, default=0.00)
    DiscountPercentage = Column(Float, default=0.00)
    DiscountMaxAmount = Column(Float, default=0.00)
    ExpiryDate = Column(DateTime(timezone=True), default=None)
    IsActive = Column(Boolean, default=True)
    Order = relationship("Order",  back_populates="Coupon", default=None)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, Code, Type,
                 DiscountValue = 0.0, DiscountPercentage = 0.0,
                 DiscountMaxAmount = 0.0, ExpiryDate = None,
                 IsActive = True):
        super().__init__()
        self.id = id
        self.Code = Code
        self.Type = Type
        self.DiscountValue = DiscountValue
        self.DiscountPercentage = DiscountPercentage
        self.DiscountMaxAmount = DiscountMaxAmount
        self.ExpiryDate = ExpiryDate
        self.IsActive = IsActive

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr