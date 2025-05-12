# import json
# import uuid
# from sqlalchemy import Column, DateTime, Integer, String, Float, Boolean, func, Enum as EnumColumn
# from sqlalchemy.orm import relationship
# from app.common.utils import generate_uuid4

# from app.database.base import Base
# from app.domain_types.enums.discount_type import DiscountTypes

# class Coupon(Base):

#     __tablename__ = "coupons"

#     id                 = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
#     Name               = Column(String(64))
#     Description        = Column(String(1024))
#     CouponCode         = Column(String(64), unique=True)
#     CouponType         = Column(String(64), default=None)
#     Discount           = Column(Float, default=0.00)
#     DiscountType       = Column(EnumColumn(DiscountTypes), default=DiscountTypes.FLAT.value)
#     DiscountPercentage = Column(Float, default=0.00)
#     DiscountMaxAmount  = Column(Float, default=0.00)
#     StartDate          = Column(DateTime(timezone=True), default=None)
#     EndDate            = Column(DateTime(timezone=True), default=None)
#     MaxUsage           = Column(Integer, default=10000)
#     MaxUsagePerUser    = Column(Integer, default=1)
#     MaxUsagePerOrder   = Column(Integer, default=1)
#     MinOrderAmount     = Column(Float, default=0.00)
#     IsActive           = Column(Boolean, default=True)
#     IsDeleted          = Column(Boolean, default=False)
#     CreatedBy          = Column(String(36), default=None)
#     CreatedAt          = Column(DateTime(timezone=True), server_default=func.now())
#     UpdatedAt          = Column(DateTime(timezone=True), onupdate=func.now())

#     # def __init__(self, id, name, description, couponCode, couponType):
#     #     super().__init__()
#     #     self.id          = id
#     #     self.Name        = name
#     #     self.Description = description
#     #     self.CouponCode  = couponCode
#     #     self.CouponType  = couponType

#     def __repr__(self):
#         jsonStr = json.dumps(self.__dict__)
#         return jsonStr



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
