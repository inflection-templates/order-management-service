from typing import Optional
from pydantic import Field
from app.database.mongodb.models.base_model import MongoDBBaseModel
from app.domain_types.enums.payment_status_types import PaymentStatusTypes

class PaymentTransactionModel(MongoDBBaseModel):
    """MongoDB Payment Transaction model"""
    OrderId: str = Field(...)
    Amount: float = Field(..., ge=0.0)
    Currency: str = Field(default="USD", max_length=3)
    PaymentMethod: str = Field(..., max_length=50)
    PaymentStatus: PaymentStatusTypes = Field(default=PaymentStatusTypes.INITIATED)  # Use INITIATED, not NONE
    TransactionReference: Optional[str] = Field(None, max_length=100)
    GatewayResponse: Optional[dict] = Field(None)
    
    class Config:
        collection_name = "payment_transactions"
        json_schema_extra = {  # Use json_schema_extra for Pydantic v2
            "example": {
                "OrderId": "order123",
                "Amount": 99.99,
                "Currency": "USD",
                "PaymentMethod": "credit_card",
                "PaymentStatus": "Initiated"
            }
        }
