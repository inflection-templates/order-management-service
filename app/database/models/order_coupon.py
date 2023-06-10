import json
import uuid
from sqlalchemy import Column, ForeignKey, String, Float, Boolean, DateTime, func
from app.database.base import Base

class OrderCoupon(Base):

    __tablename__ = "order_coupons"

    id                 = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    Code               = Column(String(64))
    CouponId           = Column(String(36), ForeignKey("coupons.id"))
    OrderId            = Column(String(36), ForeignKey("orders.id"))
    DiscountValue      = Column(Float, default=0.00)
    DiscountPercentage = Column(Float, default=0.00)
    DiscountMaxAmount  = Column(Float, default=0.00)
    Applied            = Column(Boolean, default=True)
    AppliedAt          = Column(DateTime(timezone=True), default=None)
    CreatedAt          = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt          = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, Code, OrderId,
                 DiscountValue = 0.0, DiscountPercentage = 0.0,
                 DiscountMaxAmount = 0.0, ExpiryDate = None,
                 IsActive = True):
        super().__init__()
        self.id                 = id
        self.Code               = Code
        self.OrderId            = OrderId
        self.DiscountValue      = DiscountValue
        self.DiscountPercentage = DiscountPercentage
        self.DiscountMaxAmount  = DiscountMaxAmount
        self.ExpiryDate         = ExpiryDate
        self.IsActive           = IsActive

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr