import json
from sqlmodel import SQLModel, Field, Column, DateTime, Date
from app.common.utils import generate_uuid4
from typing import Optional
from datetime import datetime, date
from sqlalchemy import func

class UserLoginSession(SQLModel, table=True):
    __tablename__ = "user_login_sessions"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    UserId: Optional[str] = Field(default=None, foreign_key="users.id", max_length=36)
    IsActive: bool = Field(default=True)
    StartedAt: Optional[date] = Field(default=None, sa_column=Column(Date))
    ValidTill: date = Field(sa_column=Column(Date))
    CreatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
    DeletedAt: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "UserId": self.UserId,
            "IsActive": self.IsActive,
            "StartedAt": str(self.StartedAt) if self.StartedAt else None,
            "ValidTill": str(self.ValidTill),
            "CreatedAt": str(self.CreatedAt),
            "UpdatedAt": str(self.UpdatedAt)
        })
