# import uuid
# from app.database.base import Base
# from app.common.utils import generate_uuid4
# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, func, Enum as EnumColumn

# class OrderPayment(Base):
#     __tablename__ = "order_payments"

#     id                   = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
#     OrderId              = Column(String(36), ForeignKey("orders.id"), default=None)
#     PaymentTransactionId = Column(String(36), ForeignKey("payment_transactions.id"), default=None)
#     RefundTransactionId  = Column(String(36), ForeignKey("payment_transactions.id"), default=None)



from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.common.utils import generate_uuid4
from datetime import datetime

from app.database.models.order import Order
from app.database.models.payment_transaction import PaymentTransaction

class OrderPayment(SQLModel, table=True):
    __tablename__ = "order_payments"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    OrderId: Optional[str] = Field(default=None, foreign_key="orders.id", max_length=36)
    PaymentTransactionId: Optional[str] = Field(default=None, foreign_key="payment_transactions.id", max_length=36)
    RefundTransactionId: Optional[str] = Field(default=None, foreign_key="payment_transactions.id", max_length=36)

    # Relationship definitions (Optional, assuming these are to be used for eager loading)
    order: Optional["Order"] = Relationship(back_populates="order_payments")
    payment_transaction: Optional["PaymentTransaction"] = Relationship(back_populates="order_payments")
    refund_transaction: Optional["PaymentTransaction"] = Relationship(back_populates="refunded_payments")

    def __repr__(self):
        return self.json(indent=2)
