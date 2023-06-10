import json
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database.database_accessor import Base
from sqlalchemy.sql import func

class Merchant(Base):

    __tablename__ = "merchants"

    id          = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    ReferenceId = Column(String(36), unique=True, default=None)
    Name        = Column(String(512), default=None)
    Email       = Column(String(512), unique=True, default=None)
    Phone       = Column(String(64), unique=True, default=None)
    Logo        = Column(String(512), default=None)
    WebsiteUrl  = Column(String(512), default=None)
    TaxNumber   = Column(String(64), unique=True, default=None)
    GSTNumber   = Column(String(64), unique=True, default=None)
    AddressId   = Column(String(36), ForeignKey("addresses.id"), default=None)
    CreatedAt   = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt   = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, ReferenceId, Name, Email, Phone,
                 Logo = None, WebsiteUrl = None,
                 TaxNumber = None, GSTNumber = None, AddressId = None):
        super().__init__()
        self.id          = id
        self.ReferenceId = ReferenceId
        self.Name        = Name
        self.Email       = Email
        self.Phone       = Phone
        self.Logo        = Logo
        self.WebsiteUrl  = WebsiteUrl
        self.TaxNumber   = TaxNumber
        self.GSTNumber   = GSTNumber
        self.AddressId   = AddressId

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
