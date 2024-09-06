
from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from datetime import datetime
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults
from app.domain_types.schemas.person.person import PersonCreateModel, PersonResponseModel
from app.domain_types.schemas.role.role import RoleResponseModel

class UserCreateModel(BaseModel):
    Person: Optional['PersonCreateModel'] = Field(default=None, description="The associated person details for the user") 
    UserName: Optional[str] = Field(default=None, description="The username of the user for login purposes")
    Password: Optional[str] = Field(default=None, description="The password for the user account")
    LastLogin: Optional[datetime] = Field(default=None, description="The timestamp of the user's last login")
    RoleId: Optional[int] = Field(default=None, description="The role identifier assigned to the user")
    
UserCreateModel.model_rebuild()

class UserUpdateModel(BaseModel):
    Person: Optional['PersonCreateModel'] = Field(default=None, description="The associated person details for the user") 
    UserName: Optional[str] = Field(default=None, description="The username of the user for login purposes")
    Password: Optional[str] = Field(default=None, description="The password for the user account")
    LastLogin: Optional[datetime] = Field(default=None, description="The timestamp of the user's last login")
    RoleId: Optional[int] = Field(default=None, description="The role identifier assigned to the user")
    
UserUpdateModel.model_rebuild()

class UserSearchFilters(BaseSearchFilter):
  Phone     : Optional[str] = Field(default=None, description="Phone number of the user")
  Email     : Optional[str] = Field(default=None, description="Email address of the user")
  UserId    : Optional[UUID4] = Field(default=None, description="ID of the user")
  UserName  : Optional[str] = Field(default=None, description="Username of the user")
  RoleIds   : Optional[List[str]] = Field(default=None, description="List of role IDs associated with the user")

UserSearchFilters.model_rebuild()
class UserResponseModel(BaseModel):
    id        : Optional[UUID4] = None
    PersonId  : Optional[UUID4] = None
    Person    : Optional[PersonResponseModel] = None
    RoleId    : Optional[int] = None
    Role      : Optional[RoleResponseModel] = None
    UserName  : Optional[str] = None
    LastLogin : Optional[datetime] = None

UserResponseModel.model_rebuild()
class UserSearchResults(BaseSearchResults):
    Items : List[PersonResponseModel] = Field(description="List of persons")