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