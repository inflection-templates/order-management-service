# import json
# import uuid
# from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float, Enum as EnumColumn
# from sqlalchemy.orm import relationship
# from app.common.utils import generate_uuid4
# from app.database.base import Base
# from sqlalchemy.sql import func
# from app.domain_types.enums.address_types import AddressTypes
# from app.database.models.address import Address
# from app.database.models.customer import Customer

# class CustomerAddress(Base):

#     __tablename__ = "customer_addresses"

#     id          = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
#     CustomerId  = Column(String(36), ForeignKey("customers.id"), default=None)
#     AddressId   = Column(String(36), ForeignKey("addresses.id"), default=None)
#     AddressType = Column(EnumColumn(AddressTypes), default=AddressTypes.SHIPPING.value)
#     IsFavorite  = Column(Boolean, default=False)

#     def __repr__(self):
#         jsonStr = json.dumps(self.__dict__)
#         return jsonStr


from sqlmodel import SQLModel, Field, Enum, Relationship
from typing import Optional
from app.common.utils import generate_uuid4
from app.domain_types.enums.address_types import AddressTypes
from app.database.models.address import Address
from app.database.models.customer import Customer


class CustomerAddress(SQLModel, table=True):
    __tablename__ = "customer_addresses"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    CustomerId: Optional[str] = Field(default=None, foreign_key="customers.id", max_length=36)
    AddressId: Optional[str] = Field(default=None, foreign_key="addresses.id", max_length=36)
    AddressType: AddressTypes = Field(default=AddressTypes.SHIPPING)
    IsFavorite: bool = Field(default=False)

    customer: Optional[Customer] = Relationship(back_populates="addresses")
    address: Optional[Address] = Relationship(back_populates="customers")

    def __repr__(self):
        return self.json(indent=2)
