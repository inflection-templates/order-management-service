from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from app.common.utils import generate_uuid4

class Cart(SQLModel, table=True):
    __tablename__ = "carts"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    CustomerId: Optional[str] = Field(default=None, max_length=36)
    TotalItemsCount: int = Field(default=0)
    TotalTax: float = Field(default=0.0)
    TotalDiscount: float = Field(default=0.0)
    TotalAmount: float = Field(default=0.0)
    CartToOrderTimestamp: Optional[datetime] = None
    AssociatedOrderId: Optional[str] = Field(default=None, max_length=36)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: Optional[datetime] = None
    DeletedAt: Optional[datetime] = None

    def __repr__(self):
        return self.json(indent=2)
