from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.enums.address_types import AddressTypes

class CustomerAddressCreateModel(BaseModel):
    CustomerId  : UUID4                  = Field(description="Id of the customer")
    AddressId   : UUID4                  = Field(description="Id of the address")
    AddressType : Optional[AddressTypes] = Field(default=AddressTypes.SHIPPING.value, description="Type of address")
    IsFavorite  : Optional[bool]         = Field(default=False, description="Is this favorite address")
