import json
import uuid
from sqlalchemy import Column, DateTime, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func

class Role(Base):

    __tablename__ = "roles"

    id           = Column(uuid, primary_key=True, index=True, default=generate_uuid4)
    RoleName     = Column(String(128), nullable=False)
    Description  = Column(String(128), nullable=True)
    CreatedAt    = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt    = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    DeletedAt    = Column(DateTime(timezone=True))
    
    persons = relationship('PersonRole', back_populates='role')
    
    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr