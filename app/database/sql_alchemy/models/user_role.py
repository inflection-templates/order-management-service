import json
import uuid
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.sql_alchemy.base import Base
from sqlalchemy.sql import func
# from app.database.models.person.person import Person
# from app.database.models.role import Role

class UserRole(Base):

    __tablename__ = "user_roles"

    id               = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    UserId           = Column(String(36),ForeignKey("users.id"), nullable=True)
    RoleId           = Column(Integer, ForeignKey("roles.id"), default=None)
    CreatedAt        = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt        = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    DeletedAt        = Column(DateTime(timezone=True))

    user = relationship('User', back_populates='user_roles')
    role = relationship("Role", back_populates='user_roles')
    
    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr