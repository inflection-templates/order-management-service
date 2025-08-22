from sqlmodel import SQLModel, Field
from app.common.utils import generate_uuid4
from datetime import datetime
from sqlmodel import Column, DateTime, Text
from sqlalchemy.sql import func

class AuthToken(SQLModel, table=True):
    __tablename__ = "auth_tokens"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    UserId: str = Field(foreign_key="users.id", max_length=36)
    TokenType: str = Field(max_length=50)
    Token: str = Field(sa_column=Column(Text))
    IsRevoked: bool = Field(default=False)
    ExpiresAt: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    CreatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))

    def __repr__(self):
        return self.json(indent=2)
