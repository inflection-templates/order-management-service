import json
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func
# from app.database.models.person.person import Person
# from app.database.models.role import Role

class User(Base):

    __tablename__ = "users"

    id               = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    Prefix           = Column(String(16), nullable=True)
    FirstName        = Column(String(70), nullable=True)
    MiddleName       = Column(String(70), nullable=True)
    LastName         = Column(String(70), nullable=True)
    Email            = Column(String(512), unique=True, default=None)
    CountryCode      = Column(String(16), nullable=True)
    Phone            = Column(String(24), unique=True, default=None)
    Gender           = Column(String(28), nullable=True)
    BirthDate        = Column(Date, nullable=True)
    Age              = Column(String(28), nullable=True)
    # RoleId           = Column(Integer, default=None)
    UserName         = Column(String(128), nullable=True)
    Password         = Column(String(256), nullable=False)
    ImageResourceId  = Column(String(36), nullable=True)
    NationalId       = Column(String(28), nullable=True)
    NationalIdType   = Column(String(28), nullable=True)
    CreatedAt        = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt        = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user_roles = relationship("UserRole", back_populates="user")

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr