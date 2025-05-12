# import json
# import uuid
# from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
# from sqlalchemy.orm import relationship
# from app.common.utils import generate_uuid4
# from app.database.base import Base
# from sqlalchemy.sql import func
# from app.database.models.address import Address

# class Customer(Base):

#     __tablename__ = "customers"

#     id                       = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
#     ReferenceId              = Column(String(36), unique=True, default=None)
#     Name                     = Column(String(128), default=None)
#     Email                    = Column(String(512), unique=True, default=None)
#     PhoneCode                = Column(String(8), default=None)
#     Phone                    = Column(String(64), unique=True, default=None)
#     ProfilePicture           = Column(String(512), default=None)
#     TaxNumber                = Column(String(64), unique=True, default=None)
#     DefaultShippingAddressId = Column(String(36), ForeignKey("addresses.id"), default=None)
#     DefaultBillingAddressId  = Column(String(36), ForeignKey("addresses.id"), default=None)
#     CreatedAt                = Column(DateTime(timezone=True), server_default=func.now())
#     UpdatedAt                = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


#     def __repr__(self):
#         jsonStr = json.dumps(self.__dict__)
#         return jsonStr


from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.common.utils import generate_uuid4
from app.database.models.address import Address


class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    ReferenceId: Optional[str] = Field(default=None, unique=True, max_length=36)
    Name: Optional[str] = Field(default=None, max_length=128)
    Email: Optional[str] = Field(default=None, unique=True, max_length=512)
    PhoneCode: Optional[str] = Field(default=None, max_length=8)
    Phone: Optional[str] = Field(default=None, unique=True, max_length=64)
    ProfilePicture: Optional[str] = Field(default=None, max_length=512)
    TaxNumber: Optional[str] = Field(default=None, unique=True, max_length=64)
    DefaultShippingAddressId: Optional[str] = Field(default=None, foreign_key="addresses.id", max_length=36)
    DefaultBillingAddressId: Optional[str] = Field(default=None, foreign_key="addresses.id", max_length=36)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow, on_update=datetime.utcnow)

    # Relationship to Address models for shipping and billing
    default_shipping_address: Optional[Address] = Relationship(sa_relationship_kwargs={"backref": "customers_shipping"})
    default_billing_address: Optional[Address] = Relationship(sa_relationship_kwargs={"backref": "customers_billing"})

    def __repr__(self):
        return self.json(indent=2)
