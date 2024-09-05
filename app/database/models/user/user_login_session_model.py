import json
import uuid
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func
from app.database.models.person.person_model import Person
from app.database.models.role.role_model import Role

class UserLoginSession(Base):

    __tablename__ = "user_login_sessions"

    id              = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    UserId          = Column(uuid, ForeignKey("users.id"), nullable=True)
    IsActive        = Column(Boolean, default=True)
    StartedAt       = Column(Date, nullable=True)
    ValidTill       = Column(Date, nullable=False)
    CreatedAt       = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt       = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    DeletedAt       = Column(DateTime(timezone=True))

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr