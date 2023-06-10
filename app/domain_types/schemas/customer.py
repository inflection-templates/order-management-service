from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.enums.order_status_types import OrderStatusTypes
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class CustomerCreateModel(BaseModel):
    ReferenceId              : UUID4                  = Field(description="Reference Id of the customer in the customer service")
    Name                     : str                    = Field(min_length=2, max_length=128, description="Name of the customer")
    Email                    : str | None             = Field(min_length=5, max_length=512, description="Email of the customer")
    PhoneCode                : Optional[str | None]   = Field(default=None, min_length=1, max_length=8, description="Phone code of the customer")
    Phone                    : Optional[str | None]   = Field(default=None, min_length=2, max_length=12, description="Phone number of the customer")
    ProfilePicture           : Optional[str | None]   = Field(default=None, min_length=5, max_length=512, description="Profile picture URL of the customer")
    TaxNumber                : Optional[str | None]   = Field(default=None, min_length=2, max_length=64, description="Tax number/code of the customer")
    DefaultShippingAddressId : Optional[UUID4 | None] = Field(default=None, description="Shipping address Id of the customer")
    DefaultBillingAddressId  : Optional[UUID4 | None] = Field(default=None, description="Billing address Id of the customer")

class CustomerUpdateModel(BaseModel):
    Name           : Optional[str] = Field(min_length=2, max_length=128, description="Name of the customer")
    Email          : Optional[str] = Field(min_length=5, max_length=512, description="Email of the customer")
    PhoneCode      : Optional[str] = Field(min_length=1, max_length=8, description="Phone code of the customer")
    Phone          : Optional[str] = Field(min_length=2, max_length=12, description="Phone number of the customer")
    ProfilePicture : Optional[str] = Field(min_length=5, max_length=512, description="Profile picture URL of the customer")
    TaxNumber      : Optional[str] = Field(min_length=2, max_length=64, description="Tax number/code of the customer")

class CustomerSearchFilter(BaseSearchFilter):
    Name           : Optional[str] = Field(description="Search by the name of the customer")
    Email          : Optional[str] = Field(description="Search by the email of the customer")
    PhoneCode      : Optional[str] = Field(description="Search by the phone code of the customer")
    Phone          : Optional[str] = Field(description="Search by the phone number of the customer")
    TaxNumber      : Optional[str] = Field(description="Search by the tax number/code of the customer")
    CreatedBefore  : Optional[datetime] = Field(description="Search customers created before the given date")
    CreatedAfter   : Optional[datetime] = Field(description="Search customers created after the given date")
    PastMonths     : Optional[int] = Field(ge=0, le=12, description="Search customers created in the past given number of months")

class CustomerResponseModel(BaseModel):
    id                       : UUID4                  = Field(description="Id of the customer")
    ReferenceId              : UUID4                  = Field(description="Reference Id of the customer in the customer service")
    Name                     : str                    = Field(description="Name of the customer")
    Email                    : str | None             = Field(description="Email of the customer")
    PhoneCode                : Optional[str | None]   = Field(default=None, description="Phone code of the customer")
    Phone                    : Optional[str | None]   = Field(default=None, description="Phone number of the customer")
    ProfilePicture           : Optional[str | None]   = Field(default=None, description="Profile picture URL of the customer")
    TaxNumber                : Optional[str | None]   = Field(default=None, description="Tax number/code of the customer")
    DefaultShippingAddressId : Optional[UUID4 | None] = Field(default=None, description="Shipping address Id of the customer")
    DefaultShippingAddress   : Optional[dict | None]   = Field(default=None, description="Shipping address of the customer")
    DefaultBillingAddressId  : Optional[UUID4 | None] = Field(default=None, description="Billing address Id of the customer")
    DefaultBillingAddress    : Optional[dict | None]   = Field(default=None, description="Billing address of the customer")
    CreatedAt                : datetime               = Field(description="Created at")
    UpdatedAt                : datetime               = Field(description="Updated at")

class CustomerSearchResults(BaseSearchResults):
    results : List[CustomerResponseModel] = Field(description="List of customers")
