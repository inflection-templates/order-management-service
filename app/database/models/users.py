from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text, Table, Enum as EnumColumn
from sqlalchemy import func
from sqlalchemy.orm import relationship
import json

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid4)
    FirstName = Column(String(64))
    LastName = Column(String(64))
    UserName = Column(String(32))
    Email = Column(String(255))
    CountryCode = Column(String(5))
    PhoneNumber = Column(String(15))
    Password = Column(String(128))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships

    def __repr__(self):
        return f"<User(id={self.id}, UserName={self.UserName})>"
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}