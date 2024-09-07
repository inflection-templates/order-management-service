from datetime import datetime
from sqlite3 import Date
from typing import List, Optional, Literal
from pydantic import UUID4, BaseModel, Field
from app.domain_types.schemas.address import AddressResponseModel
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class PersonCreateModel(BaseModel):
    Prefix             : Optional[str | None]   = Field(default=None)
    FirstName          : Optional[str | None]   = Field(default=None)
    MiddleName         : Optional[str | None]   = Field(default=None)
    LastName           : Optional[str | None]   = Field(default=None)
    CountryCode        : str                    = Field( min_length=2, max_length=64)
    Phone              : str                    = Field (max_length=10)
    Email              : str                    = Field(min_length=5, max_length=512)
    Gender             : Optional[str | None]   = Field(default=None, min_length=5, max_length=512)
    BirthDate          : Optional[str | None]   = Field(default=None, min_length=5, max_length=512)
    ImageResourceId    : Optional[UUID4]        = Field(default=None, description="Id of the image resource")
    AddressIds         : Optional[List[str]]    = Field(default=None, description="List of address IDs associated with the person"
    )
    
PersonCreateModel.model_rebuild()
 
class PersonUpdateModel(BaseModel):
    Prefix              : Optional[str | None]  = Field(default=None)
    FirstName           : Optional[str | None]  = Field(description="First name of the person")
    MiddleName          : Optional[str | None]  = Field(default=None)
    LastName            : Optional[str | None]  = Field(description="Last name of the person")
    CountryCode         : Optional[str | None]  = Field( min_length=2, max_length=64, description="Country code of the person")
    Phone               : Optional[str | None]  = Field (max_length=10, description="Phone of the person")
    Email               : Optional[str | None]  = Field(min_length=5, max_length=512, description="Email of the person")
    Gender              : Optional[str | None]  = Field(min_length=5, max_length=512)
    BirthDate           : Optional[Date | None] = Field(min_length=5, max_length=512)
    ImageResourceId     : Optional[UUID4]       = Field(description="Id of the image resource")
    AddressIds          : Optional[List[str]]   = Field(description="List of address IDs associated with the person")
   
PersonUpdateModel.model_rebuild()
 
class PersonsSearchFilter(BaseSearchFilter):
    Email          : Optional[str | None]   = Field(description="Search by the email of the person")
    Phone          : Optional[str | None]   = Field(description="Search by the phone number of the person")
    CreatedBefore  : Optional[datetime]     = Field(description="Search persons created before the given date")
    CreatedAfter   : Optional[datetime]     = Field(description="Search persons created after the given date")
    PastMonths     : Optional[int]          = Field(ge=0, le=12, description="Search persons created in the past given number of months")

PersonsSearchFilter.model_rebuild()
class PersonResponseModel(BaseModel):
    id               : UUID4
    FirstName        : str
    LastName         : str
    CountryCode      : str
    Phone            : str
    Email            : str
    Gender           : str
    BirthDate        : Date
    Addresses        : Optional[List[AddressResponseModel]]
    CreatedAt        : datetime
    UpdatedAt        : datetime
  
PersonResponseModel.model_rebuild()  
class PersonSearchResults(BaseSearchResults):
    Items : List[PersonResponseModel] = Field(description="List of persons")

class LoginModel(BaseModel):
    Email      : Optional[str | None]   = Field(min_length=5, max_length=512, description="Email of the person")
    Password   : str                    = Field(min_length=5, max_length=512, description="Password of the person")
    UserName   : Optional[str | None]   = Field(default=None, description="Name of the person")
    
class LoginResponse(BaseModel):
    person              : PersonResponseModel
    access_token        : str
    session_valid_till  : datetime    