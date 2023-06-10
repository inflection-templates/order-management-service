import json
import uuid
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from app.database.base import Base

class Cart(Base):

    __tablename__ = "carts"

    id                   = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    CustomerId           = Column(String(36), default=None)
    TotalItemsCount      = Column(Integer, default=0)
    TotalTax             = Column(Float, default=0.0)
    TotalDiscount        = Column(Float, default=0.0)
    TotalAmount          = Column(Float, default=0.0)
    CartToOrderTimestamp = Column(DateTime(timezone=True), default=None)
    AssociatedOrderId    = Column(String(36), default=None)
    CreatedAt            = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt            = Column(DateTime(timezone=True), onupdate=func.now())
    DeletedAt            = Column(DateTime(timezone=True), default=None)

    def __init__(self, id, customerId):
        super().__init__()
        self.id         = id
        self.CustomerId = customerId

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
