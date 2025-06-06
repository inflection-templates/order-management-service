from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.common.utils import generate_uuid4
from datetime import datetime

from app.database_sqlmodel.models.order import Order
from app.database_sqlmodel.models.payment_transaction import PaymentTransaction

class OrderPayment(SQLModel, table=True):
    __tablename__ = "order_payments"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    OrderId: Optional[str] = Field(default=None, foreign_key="orders.id", max_length=36)
    PaymentTransactionId: Optional[str] = Field(default=None, foreign_key="payment_transactions.id", max_length=36)
    RefundTransactionId: Optional[str] = Field(default=None, foreign_key="payment_transactions.id", max_length=36)

    order: Optional["Order"] = Relationship(back_populates="order_payments")
    payment_transaction: Optional["PaymentTransaction"] = Relationship(back_populates="order_payments")
    refund_transaction: Optional["PaymentTransaction"] = Relationship(back_populates="refunded_payments")

    def __repr__(self):
        return self.json(indent=2)
