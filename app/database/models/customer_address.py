import json
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float, Enum as EnumColumn
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func
from app.domain_types.enums.address_types import AddressTypes
from app.database.models.address import Address
from app.database.models.customer import Customer


class CustomerAddress(Base):

    __tablename__ = "customer_addresses"

    id          = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    CustomerId  = Column(String(36), ForeignKey("customers.id"), default=None)
    AddressId   = Column(String(36), ForeignKey("addresses.id"), default=None)
    AddressType = Column(EnumColumn(AddressTypes), default=AddressTypes.SHIPPING.value)
    IsFavorite  = Column(Boolean, default=False)
    CreatedAt   = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt   = Column(DateTime(timezone=True), onupdate=func.now())

    customer = relationship("Customer")
    address = relationship("Address")

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
