import json
import uuid
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database.connector import Base
from sqlalchemy.sql import func

class Address(Base):

    __tablename__ = "addresses"

    id = Column(String(36), primary_key=True, index=True, default=str(uuid.uuid4()))
    AddressLine1 = Column(String(512))
    AddressLine2 = Column(String(512))
    City = Column(String(64))
    State = Column(String(64))
    Country = Column(String(64))
    ZipCode = Column(String(64))
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, AddressLine1, AddressLine2, City, State, Country, ZipCode):
        super().__init__()
        self.id = id
        self.AddressLine1 = AddressLine1
        self.AddressLine2 = AddressLine2
        self.City = City
        self.State = State
        self.Country = Country
        self.ZipCode = ZipCode

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr

