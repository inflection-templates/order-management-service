import uuid
from app.database.base import Base
from app.common.utils import generate_uuid4
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, func, Enum as EnumColumn

class OrderPayment(Base):
    __tablename__ = "order_payments"

    id                   = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    OrderId              = Column(String(36), ForeignKey("orders.id"), default=None)
    PaymentTransactionId = Column(String(36), ForeignKey("payment_transactions.id"), default=None)
    RefundTransactionId  = Column(String(36), ForeignKey("payment_transactions.id"), default=None)