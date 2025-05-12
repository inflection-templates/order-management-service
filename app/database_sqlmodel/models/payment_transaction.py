# import json
# import uuid
# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, func, Enum as EnumColumn
# from sqlalchemy.orm import relationship
# from app.common.utils import generate_uuid4
# from app.database.base import Base
# from app.domain_types.enums.order_status_types import OrderStatusTypes
# from app.domain_types.enums.payment_status_types import PaymentStatusTypes


# class PaymentTransaction(Base):

#     __tablename__ = "payment_transactions"

#     id                          = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
#     DisplayCode                 = Column(String(36), unique=True, index=True)
#     InvoiceNumber               = Column(String(64), unique=True, index=True)
#     BankTransactionId           = Column(String(36), default=None)
#     PaymentGatewayTransactionId = Column(String(36), default=None)
#     PaymentStatus               = Column(EnumColumn(PaymentStatusTypes), default=PaymentStatusTypes.UNKNOWN.value)
#     PaymentMode                 = Column(String(36), default=None)
#     PaymentAmount               = Column(Float, default=0.0)
#     PaymentCurrency             = Column(String(36), default=None)
#     InitiatedDate               = Column(DateTime(timezone=True), default=None)
#     CompletedDate               = Column(DateTime(timezone=True), default=None)
#     PaymentResponse             = Column(String(1024), default=None)
#     PaymentResponseCode         = Column(String(36), default=None)
#     InitiatedBy                 = Column(String(36), default=None)
#     CustomerId                  = Column(String(36), ForeignKey("customers.id"), default=None)
#     OrderId                     = Column(String(36), ForeignKey("orders.id"), default=None)
#     IsRefund                    = Column(Boolean, default=False)
#     CreatedAt                   = Column(DateTime(timezone=True), server_default=func.now())
#     UpdatedAt                   = Column(DateTime(timezone=True), onupdate=func.now())

#     def __repr__(self):
#         jsonStr = json.dumps(self.__dict__)
#         return jsonStr


from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.sql import func
from app.common.utils import generate_uuid4
from app.domain_types.enums.payment_status_types import PaymentStatusTypes


class PaymentTransaction(SQLModel, table=True):
    __tablename__ = "payment_transactions"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    DisplayCode: Optional[str] = Field(default=None, index=True, unique=True, max_length=36)
    InvoiceNumber: Optional[str] = Field(default=None, index=True, unique=True, max_length=64)
    BankTransactionId: Optional[str] = Field(default=None, max_length=36)
    PaymentGatewayTransactionId: Optional[str] = Field(default=None, max_length=36)
    PaymentStatus: PaymentStatusTypes = Field(default=PaymentStatusTypes.UNKNOWN.value, sa_column_kwargs={"nullable": False})
    PaymentMode: Optional[str] = Field(default=None, max_length=36)
    PaymentAmount: float = Field(default=0.0)
    PaymentCurrency: Optional[str] = Field(default=None, max_length=36)
    InitiatedDate: Optional[datetime] = Field(default=None, sa_column_kwargs={"timezone": True})
    CompletedDate: Optional[datetime] = Field(default=None, sa_column_kwargs={"timezone": True})
    PaymentResponse: Optional[str] = Field(default=None, max_length=1024)
    PaymentResponseCode: Optional[str] = Field(default=None, max_length=36)
    InitiatedBy: Optional[str] = Field(default=None, max_length=36)
    CustomerId: Optional[str] = Field(default=None, foreign_key="customers.id", max_length=36)
    OrderId: Optional[str] = Field(default=None, foreign_key="orders.id", max_length=36)
    IsRefund: bool = Field(default=False)
    CreatedAt: datetime = Field(default_factory=func.now, sa_column_kwargs={"timezone": True})
    UpdatedAt: Optional[datetime] = Field(default=None, sa_column_kwargs={"onupdate": func.now(), "timezone": True})

    def __repr__(self):
        return self.json(indent=2)
