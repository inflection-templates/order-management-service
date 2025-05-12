# import json
# import uuid
# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, func, Enum as EnumColumn
# from sqlalchemy.orm import relationship
# from app.common.utils import generate_uuid4
# from app.database.base import Base
# from app.domain_types.enums.order_status_types import OrderStatusTypes
# from finite_state_machine import StateMachine, transition
# class Order(Base):

#     __tablename__ = "orders"

#     id                   = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
#     DisplayCode          = Column(String(36), unique=True, index=True)
#     OrderStatus          = Column(EnumColumn(OrderStatusTypes), default=OrderStatusTypes.DRAFT.value)
#     InvoiceNumber        = Column(String(64), unique=True, index=True)
#     AssociatedCartId     = Column(String(36), ForeignKey("carts.id"), default=None)
#     TotalItemsCount      = Column(Integer, default=0)
#     OrderDiscount        = Column(Float, default=0.0)
#     TipApplicable        = Column(Boolean, default=False)
#     TipAmount            = Column(Float, default=0.0)
#     TotalTax             = Column(Float, default=0.0)
#     TotalDiscount        = Column(Float, default=0.0)
#     TotalAmount          = Column(Float, default=0.0)
#     Notes                = Column(String(1024), default=None)
#     CustomerId           = Column(String(36), ForeignKey("customers.id"), default=None)
#     ShippingAddressId    = Column(String(36), ForeignKey("addresses.id"), default=None)
#     BillingAddressId     = Column(String(36), ForeignKey("addresses.id"), default=None)
#     OrderType            = Column(String(36), ForeignKey("order_types.id"), default=None)
#     CreatedAt            = Column(DateTime(timezone=True), server_default=func.now())
#     UpdatedAt            = Column(DateTime(timezone=True), onupdate=func.now())

#     def __repr__(self):
#         jsonStr = json.dumps(self.__dict__)
#         return jsonStr

# class OrderStatusMachine(StateMachine):
#     def __init__(self):
#         self.state = OrderStatusTypes.DRAFT.value
#         super().__init__()

#     @transition(source=OrderStatusTypes.DRAFT.value, target=OrderStatusTypes.INVENTRY_CHECKED.value)
#     def create_order(self):
#         print("Order Created")

#     @transition(source=OrderStatusTypes.INVENTRY_CHECKED.value, target=OrderStatusTypes.CONFIRMED.value)
#     def confirm_order(self):
#         print("Order Confirmed")

#     @transition(source=OrderStatusTypes.CONFIRMED.value, target=OrderStatusTypes.PAYMENT_INITIATED.value)
#     def initiate_payment(self):
#         print("Payment is initiated")

#     @transition(source=OrderStatusTypes.PAYMENT_INITIATED.value, target=OrderStatusTypes.PAYMENT_COMPLETED.value)
#     def complete_payment(self):
#         print("Payment completed")

#     @transition(source=OrderStatusTypes.PAYMENT_INITIATED.value, target=OrderStatusTypes.PAYMENT_FAILED.value)
#     def retry_payment(self):
#         print("Payment failed")

#     @transition(source=OrderStatusTypes.PAYMENT_COMPLETED.value, target=OrderStatusTypes.PLACED.value)
#     def placed_order(self):
#         print("Your order placed successfully!")

#     @transition(source=[OrderStatusTypes.PAYMENT_FAILED.value,
#                         OrderStatusTypes.DRAFT.value,
#                         OrderStatusTypes.CONFIRMED.value,
#                         OrderStatusTypes.PAYMENT_INITIATED.value,
#                         OrderStatusTypes.PAYMENT_COMPLETED.value,
#                         OrderStatusTypes.PLACED.value,
#                         OrderStatusTypes.SHIPPED.value
#                         ],
#                         target=OrderStatusTypes.CANCELLED.value)
#     def cancel_order(self):
#         print("Your order is cancelled")

#     @transition(source=OrderStatusTypes.PLACED.value, target=OrderStatusTypes.SHIPPED.value)
#     def shipped_order(self):
#         print("Order is shipped")

#     @transition(source=OrderStatusTypes.SHIPPED.value, target=OrderStatusTypes.DELIVERED.value)
#     def delivered_order(self):
#         print("Order delivered successfully!")

#     @transition(source=[OrderStatusTypes.DELIVERED.value,
#                         OrderStatusTypes.REFUNDED.value,
#                         OrderStatusTypes.EXCHANGED.value
#                         ],
#                         target=OrderStatusTypes.CLOSED.value)
#     def closed_order(self):
#         print("Order closed")

#     @transition(source=OrderStatusTypes.CLOSED.value, target=OrderStatusTypes.REOPENED.value)
#     def reopen_order(self):
#         print("Order reopened")

#     @transition(source=OrderStatusTypes.REOPENED.value, target=OrderStatusTypes.RETURN_INITIATED.value)
#     def initiate_return(self):
#         print("Initialized return")

#     @transition(source=OrderStatusTypes.RETURN_INITIATED.value, target=OrderStatusTypes.RETURNED.value)
#     def complete_return(self):
#         print("Return completed")

#     @transition(source=OrderStatusTypes.RETURNED.value, target=OrderStatusTypes.REFUND_INITIATED.value)
#     def initiate_refund(self):
#         print("Refund initiated")

#     @transition(source=OrderStatusTypes.REFUND_INITIATED.value, target=OrderStatusTypes.REFUNDED.value)
#     def complete_refund(self):
#         print("Refund completed")

#     @transition(source=OrderStatusTypes.REOPENED.value, target=OrderStatusTypes.EXCHANGE_INITIATED.value)
#     def initiate_exchange(self):
#         print("Exchange initiated")

#     @transition(source=OrderStatusTypes.EXCHANGE_INITIATED.value, target=OrderStatusTypes.EXCHANGED.value)
#     def complete_exchange(self):
#         print("Exchange completed")




from sqlmodel import SQLModel, Field
from sqlalchemy.sql import func
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
    CreatedAt: datetime = Field(default_factory=func.now, sa_column_kwargs={"timezone": True})
    UpdatedAt: Optional[datetime] = Field(default=None, sa_column_kwargs={"onupdate": func.now(), "timezone": True})

    def __repr__(self):
        return self.json(indent=2)
