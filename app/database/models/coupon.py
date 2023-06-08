import json
import uuid
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

from app.database.connector import Base

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    Code = Column(String(64))
    CouponType = relationship("CouponType", back_populates="Coupons", default=None)
    DiscountValue = Column(Float)
    DiscountPercentage = Column(String(64))
    DiscountMaxAmount = Column(Float)
    ExpiryDate = Column(String(64))
    IsActive = Column(Boolean)
    Order = relationship("Order", back_populates="Coupon", default=None)

    def __init__(self, id, Code, Type, DiscountValue, DiscountPercentage, DiscountMaxAmount, ExpiryDate, IsActive):
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