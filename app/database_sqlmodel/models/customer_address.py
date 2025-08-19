from sqlmodel import SQLModel, Field, Enum, Relationship
from typing import Optional
from app.common.utils import generate_uuid4
from app.domain_types.enums.address_types import AddressTypes
from app.database_sqlmodel.models.address import Address
from app.database_sqlmodel.models.customer import Customer

class CustomerAddress(SQLModel, table=True):
    __tablename__ = "customer_addresses"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    CustomerId: Optional[str] = Field(default=None, foreign_key="customers.id", max_length=36)
    AddressId: Optional[str] = Field(default=None, foreign_key="addresses.id", max_length=36)
    AddressType: AddressTypes = Field(default=AddressTypes.SHIPPING)
    IsFavorite: bool = Field(default=False)

    customer: Optional[Customer] = Relationship(back_populates="addresses")
    address: Optional[Address] = Relationship(back_populates="customers")

    def __repr__(self):
        return self.json(indent=2)
