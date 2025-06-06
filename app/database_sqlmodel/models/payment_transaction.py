from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
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
    # InitiatedDate: Optional[datetime] = Field(default=None, sa_column_kwargs={"timezone": True})
    # CompletedDate: Optional[datetime] = Field(default=None, sa_column_kwargs={"timezone": True})
    InitiatedDate: datetime = Field(default_factory=datetime.utcnow)
    CompletedDate: datetime = Field(default_factory=datetime.utcnow)
    PaymentResponse: Optional[str] = Field(default=None, max_length=1024)
    PaymentResponseCode: Optional[str] = Field(default=None, max_length=36)
    InitiatedBy: Optional[str] = Field(default=None, max_length=36)
    CustomerId: Optional[str] = Field(default=None, foreign_key="customers.id", max_length=36)
    OrderId: Optional[str] = Field(default=None, foreign_key="orders.id", max_length=36)
    IsRefund: bool = Field(default=False)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return self.json(indent=2)
