from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.common.utils import generate_uuid4
from app.database_sqlmodel.models.address import Address

class Merchant(SQLModel, table=True):
    __tablename__ = "merchants"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    ReferenceId: Optional[str] = Field(default=None, unique=True, max_length=36)
    Name: Optional[str] = Field(default=None, max_length=512)
    Email: Optional[str] = Field(default=None, unique=True, max_length=512)
    Phone: Optional[str] = Field(default=None, unique=True, max_length=64)
    Logo: Optional[str] = Field(default=None, max_length=512)
    WebsiteUrl: Optional[str] = Field(default=None, max_length=512)
    TaxNumber: Optional[str] = Field(default=None, unique=True, max_length=64)
    GSTNumber: Optional[str] = Field(default=None, unique=True, max_length=64)
    AddressId: Optional[str] = Field(default=None, foreign_key="addresses.id", max_length=36)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow)

    address: Optional[Address] = Relationship(back_populates="merchants")

    def __repr__(self):
        return self.json(indent=2)
