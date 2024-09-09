
from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from datetime import datetime
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults
from app.domain_types.schemas.person.person import PersonCreateModel, PersonResponseModel, PersonUpdateModel
from app.domain_types.schemas.role.role import RoleResponseModel

class UserCreateModel(BaseModel):
    Prefix             : Optional[str | None]   = Field(default=None)
    FirstName          : Optional[str | None]   = Field(default=None)
    MiddleName         : Optional[str | None]   = Field(default=None)
    LastName           : Optional[str | None]   = Field(default=None)
    CountryCode        : Optional[str | None]   = Field(min_length=2, max_length=64, default='+91')
    Phone              : str                    = Field (max_length=10)
    Email              : str                    = Field(min_length=5, max_length=512)
    Gender             : Optional[str | None]   = Field(default=None, min_length=5, max_length=512)
    BirthDate          : Optional[str | None]   = Field(default=None, min_length=5, max_length=512)
    ImageResourceId    : Optional[UUID4]        = Field(default=None, description="Id of the image resource")
    UserName           : Optional[str]          = Field(default=None, description="The username of the user for login purposes")
    Password           : str                    = Field(default=None, description="The password for the user account")
    RoleId             : int                    = Field(default=None, description="The role identifier assigned to the user")
    # RoleIds            : Optional[List[int]]    = Field(default=None, description="List of Role IDs associated with the user"
    # ) 
UserCreateModel.model_rebuild()

class UserUpdateModel(BaseModel):
    Prefix             : Optional[str | None]   = Field(default=None)
    FirstName          : Optional[str | None]   = Field(default=None)
    MiddleName         : Optional[str | None]   = Field(default=None)
    LastName           : Optional[str | None]   = Field(default=None)
    CountryCode        : Optional[str | None]   = Field(default=None, min_length=2, max_length=64)
    Phone              : Optional[str | None]   = Field (default=None, max_length=10)
    Email              : Optional[str | None]   = Field(default=None, min_length=5, max_length=512)
    Gender             : Optional[str | None]   = Field(default=None, min_length=5, max_length=512)
    BirthDate          : Optional[str | None]   = Field(default=None, min_length=5, max_length=512)
    ImageResourceId    : Optional[UUID4]        = Field(default=None, description="Id of the image resource")
    UserName           : Optional[str | None]   = Field(default=None, description="The username of the user for login purposes")
    Password           : Optional[str | None]   = Field(default=None, description="The password for the user account")
    RoleId             : Optional[int | None]   = Field(default=None, description="The Role id of user") 
    
UserUpdateModel.model_rebuild()

class UserSearchFilters(BaseSearchFilter):
  Phone     : Optional[str | None]  = Field(default=None, description="Phone number of the user")
  Email     : Optional[str | None]  = Field(default=None, description="Email address of the user")
  RoleId    : Optional[int | None]  = Field(default=None, description="Role id of the user")
  UserName  : Optional[str | None]  = Field(default=None, description="Username of the user")

UserSearchFilters.model_rebuild()

class UserResponseModel(BaseModel):
    id                 : UUID4         
    # RoleId             : Optional[int | None]   = Field(default=None)  
    Prefix             : Optional[str | None]   = Field(default=None)
    FirstName          : Optional[str | None]   = Field(default=None)
    MiddleName         : Optional[str | None]   = Field(default=None)
    LastName           : Optional[str | None]   = Field(default=None)
    CountryCode        : Optional[str | None]   = Field( min_length=2, max_length=64)
    Phone              : Optional[str | None]   = Field (max_length=10)
    Email              : Optional[str | None]   = Field(min_length=5, max_length=512)
    Gender             : Optional[str | None]   = Field(default=None, min_length=5, max_length=512)
    BirthDate          : Optional[str | None]   = Field(default=None, min_length=5, max_length=512)
    ImageResourceId    : Optional[UUID4]        = Field(default=None, description="Id of the image resource")
    UserName           : Optional[str]          = Field(default=None, description="The username of the user for login purposes")
    CreatedAt          : datetime               = Field(description="Created at")
    UpdatedAt          : datetime               = Field(description="Updated at")

UserResponseModel.model_rebuild()
class UserSearchResults(BaseSearchResults):
    Items : List[UserResponseModel] = Field(description="List of users")
    
class UserLoginModel(BaseModel):
    Phone              : Optional[str | None]   = Field (default=None, max_length=10)
    Email              : Optional[str | None]   = Field(default=None, min_length=5, max_length=512)
    UserName           : Optional[str | None]   = Field(default=None, description="The username of the user for login purposes")
    Password           : Optional[str | None]   = Field(default=None, description="The password for the user account")
    
UserLoginModel.model_rebuild()