import json
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float, Enum as EnumColumn
from sqlalchemy.orm import relationship
from app.database.base import Base
from sqlalchemy.sql import func
from app.domain_types.enums.address_types import AddressTypes

class CustomerAddress(Base):

    __tablename__ = "customer_addresses"

    id           = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    CustomerId   = Column(String(36), ForeignKey("customers.id"), default=None)
    AddressId    = Column(String(36), ForeignKey("addresses.id"), default=None)
    AddressType  = Column(EnumColumn(AddressTypes), default=AddressTypes.SHIPPING.value)
    IsFavorite   = Column(Boolean, default=False)

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr

