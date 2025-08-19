import json
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, Text
from app.common.utils import generate_uuid4
from app.database_alchemy.base import Base
from sqlalchemy.sql import func

class AuthToken(Base):
    __tablename__ = "auth_tokens"

    id = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    UserId = Column(String(36), ForeignKey("users.id"), nullable=False)
    TokenType = Column(String(50), nullable=False)  # access, refresh, reset_password, verify_email, invitation
    Token = Column(Text, nullable=False)
    IsRevoked = Column(Boolean, default=False)
    ExpiresAt = Column(DateTime(timezone=True), nullable=False)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "UserId": self.UserId,
            "TokenType": self.TokenType,
            "IsRevoked": self.IsRevoked,
            "ExpiresAt": self.ExpiresAt.isoformat() if self.ExpiresAt else None
        })
