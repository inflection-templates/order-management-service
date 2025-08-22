from sqlmodel import SQLModel, Field
from app.common.utils import generate_uuid4
from typing import Optional
from datetime import datetime
from sqlmodel import Column, DateTime
from sqlalchemy import func

class ApiClient(SQLModel, table=True):
    __tablename__ = "api_clients"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    ClientName: Optional[str] = Field(default=None, max_length=64)
    FirstName: Optional[str] = Field(default=None, max_length=128)
    LastName: Optional[str] = Field(default=None, max_length=128)
    ClientInterfaceType: str = Field(default='MobileApp', max_length=16)
    ClientCode: Optional[str] = Field(default=None, max_length=16)
    IsPrivileged: bool = Field(default=False)
    Password: str = Field(max_length=256)
    CountryCode: Optional[str] = Field(default=None, max_length=16)
    Phone: Optional[str] = Field(default=None, max_length=16)
    Email: str = Field(max_length=128)
    ApiKey: Optional[str] = Field(default=None, max_length=512)
    ValidFrom: Optional[datetime] = Field(default=None)
    ValidTill: Optional[datetime] = Field(default=None)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))

    def __repr__(self):
        return self.json(indent=2)
