import json
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func
from app.database.models.address import Address

class ApiClient(Base):

    __tablename__ = "api_clients"

    id                  = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    ClientName          = Column(String(64), nullable=True)
    FirstName           = Column(String(128), nullable=True)
    LastName           = Column(String(128), nullable=True)
    ClientInterfaceType = Column(String(16), nullable=False, default='MobileApp')
    ClientCode          = Column(String(16), nullable=True)
    IsPrivileged        = Column(Boolean, default=False)
    Password            = Column(String(256), nullable=False)
    CountryCode         = Column(String(16), nullable=True)
    Phone               = Column(String(16), nullable=True)
    Email               = Column(String(128), nullable=False)
    ApiKey              = Column(String(512), nullable=True)
    ValidFrom           = Column(DateTime, nullable=True)
    ValidTill           = Column(DateTime, nullable=True)
    CreatedAt           = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt           = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
   
    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr