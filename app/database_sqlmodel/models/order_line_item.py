from sqlmodel import Column, DateTime, SQLModel, Field, Relationship, func
from typing import Optional
from datetime import datetime
from app.common.utils import generate_uuid4
from app.database_sqlmodel.models.cart import Cart
from app.database_sqlmodel.models.order import Order

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
    CreatedAt: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    UpdatedAt: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )

    order: Optional["Order"] = Relationship(
        back_populates="order_line_items",
        sa_relationship_kwargs={"foreign_keys": "[OrderLineItem.OrderId]"}
    )
    cart: Optional["Cart"] = Relationship(
        back_populates="order_line_items",
        sa_relationship_kwargs={"foreign_keys": "[OrderLineItem.CartId]"}
    )

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        return self.json(indent=2)
