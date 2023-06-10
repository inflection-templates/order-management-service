import json
import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from app.database.base import Base

class OrderLineItem(Base):

    __tablename__ = "order_line_items"

    id               = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    Name             = Column(String(512))
    CatalogId        = Column(String(36), default=None)
    Quantity         = Column(Integer, default=0)
    UnitPrice        = Column(Float, default=0.0)
    Discount         = Column(Float, default=0.0)
    DiscountSchemeId = Column(String(36), default=None)
    Tax              = Column(Float, default=0.0)
    ItemSubTotal     = Column(Float, default=0.0)
    OrderId          = Column(String(36), ForeignKey("orders.id"), default=None)
    CartId           = Column(String(36), ForeignKey("carts.id"), default=None)
    CreatedAt        = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt        = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr

