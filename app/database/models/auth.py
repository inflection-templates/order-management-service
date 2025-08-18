from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text, Table, Enum as EnumColumn
from sqlalchemy import func
from sqlalchemy.orm import relationship
import json

from app.domain_types.enums.role_enum import UserRole

# from app.domain_types.enums.role_enum import UserRole

class Auth(Base):
    __tablename__ = "auth"

    id = Column(String(36), primary_key=True, default=generate_uuid4)
    Email = Column(String(255))
    Password = Column(String(128))
    Role = Column(EnumColumn(UserRole), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships

    def __repr__(self):
        return f"<Auth(id={self.id}, Email={self.Email}, Role={self.Role})>"
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}