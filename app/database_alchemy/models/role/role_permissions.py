import json
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database_alchemy.base import Base
from sqlalchemy.sql import func
# from app.database.models.role import Role

class RolePermission(Base):

    __tablename__ = "role_permissions"

    id           = Column(String(32), primary_key=True, index=True, default=generate_uuid4)
    RoleId       = Column(Integer, ForeignKey("roles.id"),nullable=False, default=None)
    RoleName     = Column(String(256), nullable=False)
    Privilege    = Column(String(512), nullable=False)
    Scope        = Column(String(32), nullable=False)
    Enabled      = Column(Boolean, default=False)
    CreatedAt    = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt    = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    DeletedAt    = Column(DateTime(timezone=True))
    
    # role = relationship(Role, back_populates='permissions')
    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr