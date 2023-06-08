import json
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database.connector import Base
from sqlalchemy.sql import func

class Customer(Base):

    __tablename__ = "customers"

    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    ReferenceId = Column(String(36), unique=True, default=None)
    Name = Column(String(512), default=None)
    Email = Column(String(512), unique=True, default=None)
    Phone = Column(String(64), unique=True, default=None)
    ProfilePicture = Column(String(512), default=None)
    TaxNumber = Column(String(64), unique=True, default=None)
    ShippingAddressId = Column(String(36), ForeignKey("addresses.id"), default=None)
    BillingAddressId = Column(String(36), ForeignKey("addresses.id"), default=None)
    Orders = relationship("Order", back_populates="Customer", default=None)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, ReferenceId, Name, Email, Phone, ProfilePicture, TaxNumber, ShippingAddressId, BillingAddressId):
        super().__init__()
        self.id = id
        self.ReferenceId = ReferenceId
        self.Name = Name
        self.Email = Email
        self.Phone = Phone
        self.ProfilePicture = ProfilePicture
        self.TaxNumber = TaxNumber
        self.ShippingAddressId = ShippingAddressId
        self.BillingAddressId = BillingAddressId

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr

