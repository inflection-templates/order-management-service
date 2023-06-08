import json
import uuid
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from app.database.connector import Base

class OrderLineItem(Base):

    __tablename__ = "order_line_items"

    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    Name = Column(String(512))
    CatalogId = Column(String(36), default=None)
    Quantity = Column(Integer, default=0)
    UnitPrice = Column(Float, default=0.0)
    Discount = Column(Float, default=0.0)
    DiscountSchemeId = Column(String(36), default=None)
    Tax = Column(Float, default=0.0)
    Total = Column(Float, default=0.0)
    Order = relationship("Order", back_populates="OrderLineItems", default=None)
    Cart = relationship("Cart", back_populates="CartLineItems", default=None)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, Name, CatalogId, Quantity, UnitPrice, Discount, Tax, Total):
        super().__init__()
        self.id = id
        self.Name = Name
        self.CatalogId = CatalogId
        self.Quantity = Quantity
        self.UnitPrice = UnitPrice
        self.Discount = Discount
        self.Tax = Tax
        self.Total = Total

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr

