from sqlmodel import Column, DateTime, SQLModel, Field, Relationship, func
from sqlmodel import Enum 
from typing import Optional
from datetime import datetime
from app.common.utils import generate_uuid4
from app.database_sqlmodel.models.order import Order
from app.domain_types.enums.order_status_types import OrderStatusTypes

class OrderHistory(SQLModel, table=True):
    __tablename__ = "order_histories"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    OrderId: str = Field(default=None, foreign_key="orders.id", max_length=36)
    PreviousStatus: OrderStatusTypes = Field(
        default=OrderStatusTypes.DRAFT.value,
        sa_column=Column(Enum(OrderStatusTypes))
    )
    Status: OrderStatusTypes = Field(
        default=OrderStatusTypes.DRAFT.value,
        sa_column=Column(Enum(OrderStatusTypes))
    )
    UpdatedByUserId: Optional[str] = Field(default=None, max_length=36)
    Timestamp: datetime = Field(default_factory=datetime.utcnow)

    order: Optional["Order"] = Relationship(back_populates="order_histories")

    def __repr__(self):
        return self.json(indent=2)
