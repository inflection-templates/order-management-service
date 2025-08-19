from sqlmodel import SQLModel, Field
from app.common.utils import generate_uuid4
from typing import Optional
from datetime import datetime
from enum import Enum
from app.domain_types.enums.order_status_types import OrderStatusTypes


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    DisplayCode: str = Field(default=None, index=True, unique=True, max_length=36)
    OrderStatus: OrderStatusTypes = Field(default=OrderStatusTypes.DRAFT.value, sa_column_kwargs={"nullable": False})
    InvoiceNumber: Optional[str] = Field(default=None, index=True, unique=True, max_length=64)
    AssociatedCartId: Optional[str] = Field(default=None, foreign_key="carts.id", max_length=36)
    TotalItemsCount: int = Field(default=0)
    OrderDiscount: float = Field(default=0.0)
    TipApplicable: bool = Field(default=False)
    TipAmount: float = Field(default=0.0)
    TotalTax: float = Field(default=0.0)
    TotalDiscount: float = Field(default=0.0)
    TotalAmount: float = Field(default=0.0)
    Notes: Optional[str] = Field(default=None, max_length=1024)
    CustomerId: Optional[str] = Field(default=None, foreign_key="customers.id", max_length=36)
    ShippingAddressId: Optional[str] = Field(default=None, foreign_key="addresses.id", max_length=36)
    BillingAddressId: Optional[str] = Field(default=None, foreign_key="addresses.id", max_length=36)
    OrderType: Optional[str] = Field(default=None, foreign_key="order_types.id", max_length=36)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return self.json(indent=2)
