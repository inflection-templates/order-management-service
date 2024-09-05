import json
import uuid
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func
from app.database.models.person.person_model import Person
from app.database.models.general.address import Address

class PersonAddresses(Base):

    __tablename__ = "person_addresses"

    id               = Column(uuid, primary_key=True, index=True, default=generate_uuid4)
    PersonId         = Column(String(70),ForeignKey("persons.id"), nullable=False)
    AddressId        = Column(String(36), ForeignKey("addresses.id"), nullable=False)
    AddressType      = Column(String(70), nullable=False)
    CreatedAt        = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt        = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    DeletedAt        = Column(DateTime(timezone=True))

    person = relationship(Person, back_populates='roles')
    addresse = relationship(Address, back_populates='addresses')
    
    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr