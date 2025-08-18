import json
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Boolean, Integer
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func

class Otp(Base):

    __tablename__ = "otps"

    id              = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    UserId          = Column(String(36), ForeignKey("users.id"), nullable=False)
    Code            = Column(String(6), nullable=False)
    Purpose         = Column(String(64), nullable=False)  # login, phone_verification, email_verification, password_reset
    PhoneNumber     = Column(String(24), nullable=True)
    Email           = Column(String(512), nullable=True)
    IsUsed          = Column(Boolean, default=False)
    AttemptCount    = Column(Integer, default=0)
    ExpiresAt       = Column(DateTime(timezone=True), nullable=False)
    CreatedAt       = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt       = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
