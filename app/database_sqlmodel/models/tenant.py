from sqlmodel import SQLModel, Field
from app.common.utils import generate_uuid4
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, DateTime, Text
from sqlalchemy.sql import func

class Tenant(SQLModel, table=True):
    __tablename__ = "tenants"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    Name: str = Field(max_length=255)
    Code: str = Field(unique=True, max_length=50)
    Description: Optional[str] = Field(default=None, sa_column=Column(Text))
    IsActive: bool = Field(default=True)
    IsDefault: bool = Field(default=False)
    Settings: Optional[str] = Field(default=None, sa_column=Column(Text))
    CreatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))

    def __repr__(self):
        return self.json(indent=2)
