import json
import uuid
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.sql_alchemy.base import Base
from sqlalchemy.sql import func
from app.database.sql_alchemy.models.person.person import Person
from app.database.sql_alchemy.models.role import Role

class Customer(Base):

    __tablename__ = "customers"

    id                        = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    UserId                    = Column(String(70),ForeignKey("users.id"), nullable=True)
    DefaultShippingAddressId  = Column(String(36), ForeignKey("addresses.id"), default=None)
    DefaultBillingAddressId   = Column(String(36), ForeignKey("addresses.id"), default=None)
    CreatedAt                 = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt                 = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    DeletedAt                 = Column(DateTime(timezone=True))

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr