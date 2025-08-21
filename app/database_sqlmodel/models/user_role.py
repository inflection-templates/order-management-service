from sqlmodel import SQLModel, Field
from app.common.utils import generate_uuid4
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    UserId: Optional[str] = Field(default=None, foreign_key="users.id", max_length=36)
    RoleId: Optional[int] = Field(default=None, foreign_key="roles.id")
    CreatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
    DeletedAt: Optional[datetime] = Field(default=None)

    def __repr__(self):
        return self.json(indent=2)