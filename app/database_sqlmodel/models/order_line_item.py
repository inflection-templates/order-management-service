# import json
# import uuid
# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, func
# from sqlalchemy.orm import relationship
# from app.common.utils import generate_uuid4
# from app.database.base import Base

# class OrderLineItem(Base):

#     __tablename__ = "order_line_items"

#     id               = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
#     Name             = Column(String(512))
#     CatalogId        = Column(String(36), default=None)
#     Quantity         = Column(Integer, default=0)
#     UnitPrice        = Column(Float, default=0.0)
#     Discount         = Column(Float, default=0.0)
#     DiscountSchemeId = Column(String(36), default=None)
#     Tax              = Column(Float, default=0.0)
#     ItemSubTotal     = Column(Float, default=0.0)
#     OrderId          = Column(String(36), ForeignKey("orders.id"), default=None)
#     CartId           = Column(String(36), ForeignKey("carts.id"), default=None)
#     CreatedAt        = Column(DateTime(timezone=True), server_default=func.now())
#     UpdatedAt        = Column(DateTime(timezone=True), onupdate=func.now())

#     def __repr__(self):
#         jsonStr = json.dumps(self.__dict__)
#         return jsonStr

from sqlmodel import Column, DateTime, SQLModel, Field, Relationship, func
from typing import Optional
from datetime import datetime
from app.common.utils import generate_uuid4
from app.database.models.cart import Cart
from app.database.models.order import Order


class OrderLineItem(SQLModel, table=True):
    __tablename__ = "order_line_items"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    Name: str = Field(default=None, max_length=512)
    CatalogId: Optional[str] = Field(default=None, max_length=36)
    Quantity: int = Field(default=0)
    UnitPrice: float = Field(default=0.0)
    Discount: float = Field(default=0.0)
    DiscountSchemeId: Optional[str] = Field(default=None, max_length=36)
    Tax: float = Field(default=0.0)
    ItemSubTotal: float = Field(default=0.0)
    OrderId: str = Field(default=None, foreign_key="orders.id", max_length=36)
    CartId: str = Field(default=None, foreign_key="carts.id", max_length=36)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    UpdatedAt: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), onupdate=func.now()))

    # Relationship to Order model (Assuming you want to relate it to an Order model)
    order: Optional["Order"] = Relationship(back_populates="order_line_items")
    cart: Optional["Cart"] = Relationship(back_populates="order_line_items")

    def __repr__(self):
        return self.json(indent=2)
