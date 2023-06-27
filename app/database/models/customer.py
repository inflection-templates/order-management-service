import json
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func
from app.database.models.address import Address

class Customer(Base):

    __tablename__ = "customers"

    id                       = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    ReferenceId              = Column(String(36), unique=True, default=None)
    Name                     = Column(String(128), default=None)
    Email                    = Column(String(512), unique=True, default=None)
    PhoneCode                = Column(String(8), default=None)
    Phone                    = Column(String(64), unique=True, default=None)
    ProfilePicture           = Column(String(512), default=None)
    TaxNumber                = Column(String(64), unique=True, default=None)
    DefaultShippingAddressId = Column(String(36), ForeignKey("addresses.id"), default=None)
    DefaultBillingAddressId  = Column(String(36), ForeignKey("addresses.id"), default=None)
    CreatedAt                = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt                = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
