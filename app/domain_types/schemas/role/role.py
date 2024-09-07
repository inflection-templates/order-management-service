import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class RoleCreateModel(BaseModel):
  RoleName    : str                   = Field(min_length=2, max_length=256, description='Name of the user role')
  Description : Optional[str | None]  = Field(min_length=2, max_length=1024, default=None, description='Description of user role')

RoleCreateModel.model_rebuild()
class RoleUpdateModel(BaseModel):
  RoleName    : Optional[str]  = Field(min_length=2, max_length=256)
  Description : Optional[str]  = Field(min_length=2, max_length=1024)

RoleUpdateModel.model_rebuild()

class RoleSearchFilter(BaseSearchFilter):
  RoleName    : Optional[str] = Field(default=None, description="Search by the name of the role")
  Description : Optional[str] = Field(default=None, description="Search by the description of the role")

class RoleResponseModel(BaseModel):
  id          : int
  RoleName    : str
  Description : Optional[str]
  # CreatedAt   : datetime
  # UpdatedAt   : datetime
  
RoleResponseModel.model_rebuild()

class RoleSearchResults(BaseSearchResults):
  Items: List[RoleResponseModel] = []
