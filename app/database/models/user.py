import json
import uuid
from sqlalchemy import Column, DateTime, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func

class User(Base):

    __tablename__ = "users"

    id           = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    FirstName    = Column(String(128), nullable=True)
    LastName     = Column(String(128), nullable=True)
    UserName     = Column(String(128), nullable=True)
    Email        = Column(String(512), unique=True, default=None)
    CountryCode  = Column(String(16), nullable=True)
    Phone        = Column(String(64), unique=True, default=None)
    Password     = Column(String(256), nullable=False)
    CreatedAt    = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt    = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr