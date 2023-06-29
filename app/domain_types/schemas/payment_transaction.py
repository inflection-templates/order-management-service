from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.enums.payment_status_types import PaymentStatusTypes
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class PaymentTransactionCreateModel(BaseModel):
    DisplayCode                 : str                  = Field(...)
    InvoiceNumber               : str                  = Field(...)
    BankTransactionId           : str                  = Field(default=None, description="Transaction Id of bank")
    PaymentGatewayTransactionId : str                  = Field(default=None, description="Transaction Id of payment gateway")
    PaymentStatus               : PaymentStatusTypes   = Field(default=PaymentStatusTypes.UNKNOWN.value, description="Status of payment")
    PaymentMode                 : str                  = Field(default=None, description="Mode of payment")
    PaymentAmount               : float                = Field(default=0.0, description="Amount to pay")
    PaymentCurrency             : str                  = Field(default=None, description="Currency of payment")
    InitiatedDate               : datetime             = Field(default=datetime.now(), description="Payment initiated date")
    CompletedDate               : datetime             = Field(description="Payment completed date")
    PaymentResponse             : str                  = Field(description="Response of payment")
    PaymentResponseCode         : str                  = Field(description="Response code of payment")
    InitiatedBy                 : str                  = Field(...)
    CustomerId                  : UUID4                = Field(description="Id of customer who did payment")
    OrderId                     : UUID4                = Field(description="Id of order for which payment is done")

class PaymentTransactionSearchFilter(BaseSearchFilter):
    DisplayCode                 : Optional[str]        = Field(description="Search by display code")
    InvoiceNumber               : Optional[str]        = Field(...)
    BankTransactionId           : Optional[str]        = Field(description="Search by bank transaction id")
    InitiatedDate               : Optional[datetime]   = Field(description="Search by payment initiated date")
    CustomerId                  : Optional[UUID4]      = Field(description="Search by id of customer who did payment")
    OrderId                     : Optional[UUID4]      = Field(description="Search by id of order")
    PaymentMode                 : Optional[str]        = Field(description="Search by mode of payment")
    PaymentAmount               : Optional[float]      = Field(description="Search by payment amount")

class PaymentTransactionResponseModel(BaseModel):
    id                          : UUID4                = Field(description="Id of payment transaction")
    DisplayCode                 : str                  = Field(...)
    InvoiceNumber               : str                  = Field(description="Number of invoice")
    BankTransactionId           : str                  = Field(default=None, description="Transaction Id of bank")
    PaymentGatewayTransactionId : str                  = Field(default=None, description="Transaction Id of payment gateway")
    PaymentStatus               : PaymentStatusTypes   = Field(default=PaymentStatusTypes.UNKNOWN.value, description="Status of payment")
    PaymentMode                 : str                  = Field(default=None, description="Mode of payment")
    PaymentAmount               : float                = Field(default=0.0, description="Amount to pay")
    PaymentCurrency             : str                  = Field(default=None, description="Currency of payment")
    InitiatedDate               : datetime             = Field(default=datetime.now(), description="Payment initiated date")
    CompletedDate               : datetime             = Field(description="Payment completed date")
    PaymentResponse             : str                  = Field(description="Response of payment")
    PaymentResponseCode         : str                  = Field(description="Response code of payment")
    InitiatedBy                 : str                  = Field(...)
    CustomerId                  : UUID4                = Field(description="Id of customer who did payment")
    OrderId                     : UUID4                = Field(description="Id of order for which payment is done")
    CreatedAt                   : Optional[datetime]   = Field(default=None, description="Order creation date")
    UpdatedAt                   : Optional[datetime]   = Field(default=None, description="Order last updated date")

