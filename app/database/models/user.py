import json
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Float, Boolean, Text
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func
# from app.database.models.person.person import Person
# from app.database.models.role import Role

class User(Base):

    __tablename__ = "users"

    id               = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    TenantId         = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    Prefix           = Column(String(16), nullable=True)
    FirstName        = Column(String(70), nullable=True)
    MiddleName       = Column(String(70), nullable=True)
    LastName         = Column(String(70), nullable=True)
    Email            = Column(String(512), nullable=True)
    CountryCode      = Column(String(16), nullable=True)
    Phone            = Column(String(24), nullable=True)
    Gender           = Column(String(28), nullable=True)
    BirthDate        = Column(Date, nullable=True)
    Age              = Column(String(28), nullable=True)
    # RoleId           = Column(Integer, default=None)
    UserName         = Column(String(128), nullable=True)
    Password         = Column(String(256), nullable=True)  # Nullable for social logins
    ImageResourceId  = Column(String(36), nullable=True)
    NationalId       = Column(String(28), nullable=True)
    NationalIdType   = Column(String(28), nullable=True)

    # Authentication fields
    IsActive         = Column(Boolean, default=True)
    IsEmailVerified  = Column(Boolean, default=False)
    IsPhoneVerified  = Column(Boolean, default=False)
    IsTwoFactorEnabled = Column(Boolean, default=False)
    TwoFactorSecret  = Column(String(32), nullable=True)  # TOTP secret
    LastLoginAt      = Column(DateTime(timezone=True), nullable=True)
    FailedLoginAttempts = Column(Integer, default=0)
    LockedUntil      = Column(DateTime(timezone=True), nullable=True)

    # External provider fields
    ExternalProviders = Column(Text, nullable=True)  # JSON array of connected providers

    CreatedAt        = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt        = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    user_roles = relationship("UserRole", back_populates="user")
    login_sessions = relationship("UserLoginSession", backref="user")
    otps = relationship("Otp", backref="user")

    def __repr__(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr
