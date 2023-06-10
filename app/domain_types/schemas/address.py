from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class AddressCreateModel(BaseModel):
    AddressLine1: str           = Field(..., min_length=2, max_length=512)
    AddressLine2: Optional[str] = Field(default=None, min_length=2, max_length=512)
    City        : str           = Field(..., min_length=2, max_length=64)
    State       : Optional[str] = Field(default=None, min_length=2, max_length=64)
    Country     : Optional[str] = Field(default=None, min_length=2, max_length=32)
    ZipCode     : Optional[str] = Field(default=None, min_length=2, max_length=32)

class AddressUpdateModel(BaseModel):
    AddressLine1: Optional[str] = Field(default=None, min_length=2, max_length=512)
    AddressLine2: Optional[str] = Field(default=None, min_length=2, max_length=512)
    City        : Optional[str] = Field(default=None, min_length=2, max_length=64)
    State       : Optional[str] = Field(default=None, min_length=2, max_length=64)
    Country     : Optional[str] = Field(default=None, min_length=2, max_length=32)
    ZipCode     : Optional[str] = Field(default=None, min_length=2, max_length=32)

class AddressSearchFilter(BaseSearchFilter):
    AddressLine : Optional[str] = Field(default=None, min_length=2, max_length=512)
    City        : Optional[str] = Field(default=None, min_length=2, max_length=64)
    State       : Optional[str] = Field(default=None, min_length=2, max_length=64)
    Country     : Optional[str] = Field(default=None, min_length=2, max_length=32)
    ZipCode     : Optional[str] = Field(default=None, min_length=2, max_length=32)

class AddressResponseModel(BaseModel):
    id          : UUID4
    AddressLine1: str
    AddressLine2: str
    City        : str
    State       : str
    Country     : str
    ZipCode     : str
    CreatedAt   : datetime
    UpdatedAt   : datetime

class AddressSearchResults(BaseSearchResults):
    Addresses: List[AddressResponseModel] = []

