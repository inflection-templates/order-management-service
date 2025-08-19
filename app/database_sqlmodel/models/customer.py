from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from app.common.utils import generate_uuid4
from app.database_sqlmodel.models.address import Address  # Make sure this is a SQLModel

class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    ReferenceId: Optional[str] = Field(default=None, unique=True, max_length=36)
    Name: Optional[str] = Field(default=None, max_length=128)
    Email: Optional[str] = Field(default=None, unique=True, max_length=512)
    PhoneCode: Optional[str] = Field(default=None, max_length=8)
    Phone: Optional[str] = Field(default=None, unique=True, max_length=64)
    ProfilePicture: Optional[str] = Field(default=None, max_length=512)
    TaxNumber: Optional[str] = Field(default=None, unique=True, max_length=64)

    DefaultShippingAddressId: Optional[str] = Field(
        default=None, foreign_key="addresses.id", max_length=36
    )
    DefaultBillingAddressId: Optional[str] = Field(
        default=None, foreign_key="addresses.id", max_length=36
    )

    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow)

    default_shipping_address: Optional[Address] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Customer.DefaultShippingAddressId]", "backref": "customers_shipping"}
    )
    default_billing_address: Optional[Address] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Customer.DefaultBillingAddressId]", "backref": "customers_billing"}
    )

    def __repr__(self):
        return self.json(indent=2)
