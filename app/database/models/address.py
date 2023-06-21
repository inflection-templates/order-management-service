import json
from sqlalchemy import Column, DateTime, String
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func


class Address(Base):

    __tablename__ = "addresses"

    id = Column(String(36), primary_key=True,
                index=True, default=generate_uuid4)
    AddressLine1 = Column(String(512))
    AddressLine2 = Column(String(512), default=None)
    City = Column(String(64))
    State = Column(String(64), default=None)
    Country = Column(String(64), default=None)
    ZipCode = Column(String(64), default=None)
    CreatedBy = Column(String(36), default=None)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
