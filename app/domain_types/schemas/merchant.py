from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.enums.order_status_types import OrderStatusTypes
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class MerchantCreateModel(BaseModel):
    ReferenceId              : UUID4                  = Field(description="Reference Id of the merchant in the merchant service")
    Name                     : str                    = Field(min_length=5, max_length=512, description="Name of the merchant")
    Email                    : str | None             = Field(min_length=5, max_length=512, description="Email of the merchant")
    Phone                    : str | None             = Field(default=None, min_length=2, max_length=12, description="Phone number of the merchant")
    Logo                     : Optional[str | None]   = Field(default=None, min_length=5, max_length=512, description="Logo URL of the merchant")
    WebsiteUrl               : Optional[str | None]   = Field(default=None, min_length=5, max_length=512, description="Website URL of the merchant")
    TaxNumber                : Optional[str | None]   = Field(default=None, min_length=2, max_length=64, description="Tax number/code of the merchant")
    GSTNumber                : Optional[str | None]   = Field(default=None, min_length=2, max_length=64, description="GST number/code of the merchant")
    AddressId                : Optional[UUID4 | None] = Field(default=None, description="Address Id of the merchant")

class MerchantUpdateModel(BaseModel):
    Name           : Optional[str]   = Field(min_length=5, max_length=512, description="Name of the merchant")
    Email          : Optional[str]   = Field(min_length=5, max_length=512, description="Email of the merchant")
    Phone          : Optional[str]   = Field(min_length=2, max_length=12, description="Phone number of the merchant")
    Logo           : Optional[str]   = Field(default=None, min_length=5, max_length=512, description="Logo URL of the merchant")
    TaxNumber      : Optional[str]   = Field(min_length=2, max_length=64, description="Tax number/code of the customer")
    GSTNumber      : Optional[str]   = Field(default=None, min_length=2, max_length=64, description="GST number/code of the merchant")
    AddressId      : Optional[UUID4] = Field(default=None, description="Address Id of the merchant")

class MerchantSearchFilter(BaseSearchFilter):
    Name           : Optional[str] = Field(description="Search by the name of the merchant")
    Email          : Optional[str] = Field(description="Search by the email of the merchant")
    Phone          : Optional[str] = Field(description="Search by the phone number of the merchant")
    TaxNumber      : Optional[str] = Field(description="Search by the tax number/code of the merchant")
    CreatedBefore  : Optional[datetime] = Field(description="Search merchants created before the given date")
    CreatedAfter   : Optional[datetime] = Field(description="Search merchants created after the given date")
    PastMonths     : Optional[int] = Field(ge=0, le=12, description="Search merchants created in the past given number of months")

class MerchantResponseModel(BaseModel):
    id                       : UUID4                  = Field(description="Id of the merchant")
    ReferenceId              : UUID4                  = Field(description="Reference Id of the merchant in the merchant service")
    Name                     : str                    = Field(min_length=5, max_length=512, description="Name of the merchant")
    Email                    : str | None             = Field(min_length=5, max_length=512, description="Email of the merchant")
    Phone                    : str | None             = Field(default=None, min_length=2, max_length=12, description="Phone number of the merchant")
    Logo                     : Optional[str | None]   = Field(default=None, min_length=5, max_length=512, description="Logo URL of the merchant")
    WebsiteUrl               : Optional[str | None]   = Field(default=None, min_length=5, max_length=512, description="Website URL of the merchant")
    TaxNumber                : Optional[str | None]   = Field(default=None, min_length=2, max_length=64, description="Tax number/code of the merchant")
    GSTNumber                : Optional[str | None]   = Field(default=None, min_length=2, max_length=64, description="GST number/code of the merchant")
    AddressId                : Optional[UUID4 | None] = Field(default=None, description="Address Id of the merchant")
    CreatedAt                : datetime               = Field(description="Created at")
    UpdatedAt                : datetime               = Field(description="Updated at")

class MerchantSearchResults(BaseSearchResults):
    results : List[MerchantCreateModel] = Field(description="List of customers")