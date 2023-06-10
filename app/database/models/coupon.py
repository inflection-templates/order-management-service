import json
import uuid
from sqlalchemy import Column, DateTime, Integer, String, Float, Boolean, func, Enum as EnumColumn
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.domain_types.enums.discount_type import DiscountTypes

class Coupon(Base):

    __tablename__ = "coupons"

    id                 = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    Name               = Column(String(64))
    Description        = Column(String(1024))
    CouponCode         = Column(String(64), unique=True)
    CouponType         = Column(String(64), default=None)
    Discount           = Column(Float, default=0.00)
    DiscountType       = Column(EnumColumn(DiscountTypes), default=DiscountTypes.FLAT.value)
    DiscountPercentage = Column(Float, default=0.00)
    DiscountMaxAmount  = Column(Float, default=0.00)
    StartDate          = Column(DateTime(timezone=True), default=None)
    EndDate            = Column(DateTime(timezone=True), default=None)
    MaxUsage           = Column(Integer, default=10000)
    MaxUsagePerUser    = Column(Integer, default=1)
    MaxUsagePerOrder   = Column(Integer, default=1)
    MinOrderAmount     = Column(Float, default=0.00)
    IsActive           = Column(Boolean, default=True)
    IsDeleted          = Column(Boolean, default=False)
    CreatedBy          = Column(String(36), default=None)
    CreatedAt          = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt          = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, name, description, couponCode, couponType):
        super().__init__()
        self.id          = id
        self.Name        = name
        self.Description = description
        self.CouponCode  = couponCode
        self.CouponType  = couponType

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
