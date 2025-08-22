from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlmodel import Column, DateTime
from sqlalchemy.sql import func

class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    RoleName: str = Field(max_length=128)
    Description: Optional[str] = Field(default=None, max_length=128)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))

    def __repr__(self):
        return self.json(indent=2)