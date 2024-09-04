from datetime import datetime
from typing import List, Optional, Literal
from pydantic import UUID4, BaseModel, Field
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class UserCreateModel(BaseModel):
    FirstName             : Optional[str | None] = Field(default=None, description="First name of the user")
    LastName              : Optional[str | None] = Field(default=None, description="Last name of the user")
    CountryCode           : str = Field( min_length=2, max_length=64, description="Country code of the user")
    Phone                 : str = Field (max_length=10, description="Phone of the user")
    Email                 : str = Field(min_length=5, max_length=512, description="Email of the user")
    Password              : str = Field(min_length=5, max_length=512, description="Password of the user")
    UserName            : Optional[str | None] = Field(default=None, description="Name of the user")
    
class UserUpdateModel(BaseModel):
    FirstName           : Optional[str | None] = Field(description="First name of the user")
    LastName            : Optional[str | None] = Field(description="Last name of the user")
    CountryCode         : Optional[str | None]  = Field( min_length=2, max_length=64, description="Country code of the user")
    Phone               : Optional[str | None]  = Field (max_length=10, description="Phone of the user")
    Email               : Optional[str | None]  = Field(min_length=5, max_length=512, description="Email of the user")
    Password            : Optional[str | None]  = Field(min_length=5, max_length=512, description="Password of the user")
   

class UsersSearchFilter(BaseSearchFilter):
    FirstName      : Optional[str | None] = Field(description="Search by the first name of the user")
    Email          : Optional[str | None] = Field(description="Search by the email of the user")
    Phone          : Optional[str | None] = Field(description="Search by the phone number of the user")
    userCode       : Optional[str | None] = Field(description="Search by the code of the user")
    CreatedBefore  : Optional[datetime] = Field(description="Search users created before the given date")
    CreatedAfter   : Optional[datetime] = Field(description="Search users created after the given date")
    PastMonths     : Optional[int] = Field(ge=0, le=12, description="Search users created in the past given number of months")

class UserResponseModel(BaseModel):
    id                    : UUID4 = Field(description="Id of the Apiuser")
    FirstName             : Optional[str | None] = Field(default=None, description="First name of the user")
    LastName              : Optional[str | None] = Field(default=None, description="Last name of the user")
    CountryCode           : str = Field( min_length=2, max_length=64, description="Country code of the user")
    Phone                 : str = Field (max_length=10, description="Phone of the user")
    Email                 : str = Field(min_length=5, max_length=512, description="Email of the user")
    UserName            : Optional[str | None] = Field(default=None, description="Name of the user")
    CreatedAt             : datetime = Field(description="Created at")
    UpdatedAt             : datetime = Field(description="Updated at")

class UserSearchResults(BaseSearchResults):
    Items : List[UserResponseModel] = Field(description="List of users")

class LoginModel(BaseModel):
    Email                 : Optional[str | None] = Field(min_length=5, max_length=512, description="Email of the user")
    Password              : str = Field(min_length=5, max_length=512, description="Password of the user")
    UserName              : Optional[str | None] = Field(default=None, description="Name of the user")
    
class LoginResponse(BaseModel):
    user: UserResponseModel
    access_token: str
    session_valid_till: datetime    