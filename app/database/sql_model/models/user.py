from sqlmodel import SQLModel, Field
from app.common.utils import generate_uuid4
from typing import Optional, List
from datetime import datetime, date
from sqlmodel import Column, DateTime
from sqlalchemy.sql import func

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    TenantId: str = Field(foreign_key="tenants.id", max_length=36, nullable=True)
    Prefix: Optional[str] = Field(default=None, max_length=16)
    FirstName: Optional[str] = Field(default=None, max_length=70)
    MiddleName: Optional[str] = Field(default=None, max_length=70)
    LastName: Optional[str] = Field(default=None, max_length=70)
    Email: Optional[str] = Field(default=None, max_length=512)
    CountryCode: Optional[str] = Field(default=None, max_length=16)
    Phone: Optional[str] = Field(default=None, max_length=24)
    Gender: Optional[str] = Field(default=None, max_length=28)
    BirthDate: Optional[date] = Field(default=None)
    Age: Optional[str] = Field(default=None, max_length=28)
    UserName: Optional[str] = Field(default=None, max_length=128)
    Password: Optional[str] = Field(default=None, max_length=256)
    ImageResourceId: Optional[str] = Field(default=None, max_length=36)
    NationalId: Optional[str] = Field(default=None, max_length=28)
    IsTwoFactorEnabled: bool = Field(default=False)
    IsEmailVerified: bool = Field(default=False)
    IsPhoneVerified: bool = Field(default=False)
    IsActive: bool = Field(default=True)
    PasswordResetToken: Optional[str] = Field(default=None, max_length=256)
    PasswordResetTokenExpiresAt: Optional[datetime] = Field(default=None)
    EmailVerificationToken: Optional[str] = Field(default=None, max_length=256)
    EmailVerificationTokenExpiresAt: Optional[datetime] = Field(default=None)
    LastLoginAt: Optional[datetime] = Field(default=None)
    FailedLoginAttempts: int = Field(default=0)
    LockedUntil: Optional[datetime] = Field(default=None)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
    DeletedAt: Optional[datetime] = Field(default=None)

    def __repr__(self):
        return self.json(indent=2)