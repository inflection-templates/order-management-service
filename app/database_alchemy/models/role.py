import json
from sqlalchemy import Column, DateTime, Integer, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database_alchemy.base import Base
from sqlalchemy.sql import func

# from app.database.models.person.person_role import PersonRole

class Role(Base):

    __tablename__ = "roles"

    id           = Column(Integer, primary_key=True, index=True)
    RoleName     = Column(String(128), nullable=False)
    Description  = Column(String(128), nullable=True)
    CreatedAt    = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt    = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user_roles = relationship("UserRole", back_populates="role")
    
    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr