import json
import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, func, Enum as EnumColumn
from sqlalchemy.orm import relationship
from app.database.base import Base
from app.domain_types.enums.order_status_types import OrderStatusTypes
from app.domain_types.enums.payment_status_types import PaymentStatusTypes


class PaymentTransaction(Base):

    __tablename__ = "payment_transactions"

    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    DisplayCode = Column(String(36), unique=True, index=True)
    InvoiceNumber = Column(String(64), unique=True, index=True)
    BankTransactionId = Column(String(36), default=None)
    PaymentGatewayTransactionId = Column(String(36), default=None)
    PaymentStatus = Column(EnumColumn(PaymentStatusTypes), default=PaymentStatusTypes.UNKNOWN.value)
    PaymentMode = Column(String(36), default=None)
    PaymentAmount = Column(Float, default=0.0)
    PaymentCurrency = Column(String(36), default=None)
    InitiatedDate = Column(DateTime(timezone=True), default=None)
    CompletedDate = Column(DateTime(timezone=True), default=None)
    PaymentResponse = Column(String(1024), default=None)
    PaymentResponseCode = Column(String(36), default=None)
    InitiatedBy = Column(String(36), default=None)
    CustomerId = Column(String(36), ForeignKey("customers.id"), default=None)
    OrderId = Column(String(36), ForeignKey("orders.id"), default=None)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
