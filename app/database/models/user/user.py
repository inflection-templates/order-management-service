import json
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func
# from app.database.models.person.person import Person
# from app.database.models.role import Role

class User(Base):

    __tablename__ = "users"

    id           = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    UserName     = Column(String(128), nullable=True)
    PersonId     = Column(String(70),ForeignKey("persons.id"), nullable=True)
    RoleId       = Column(String(36), ForeignKey("roles.id"), default=None)
    RoleName     = Column(String(70), nullable=False)
    Password     = Column(String(256), nullable=False)
    LastLogin    = Column(Date, nullable=False)
    CreatedAt    = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt    = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr