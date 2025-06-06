from sqlmodel import SQLModel, Field
from sqlalchemy.sql import func
from app.common.utils import generate_uuid4
from typing import Optional
from datetime import datetime

class OrderType(SQLModel, table=True):
    __tablename__ = "order_types"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    Name: str = Field(..., max_length=128)
    Description: Optional[str] = Field(default=None, max_length=64)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return self.json(indent=2)
