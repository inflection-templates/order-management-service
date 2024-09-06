from typing import Optional
from pydantic import UUID4, BaseModel, Field

class RoleCreateModel(BaseModel):
  RoleName    : str = Field(min_length=2, max_length=256, description='Name of the user role')
  Description : str = Field(min_length=2, max_length=1024, description='Description of user role')

RoleCreateModel.model_rebuild()
class RoleUpdateModel(BaseModel):
    RoleName    : Optional[str]  = Field(min_length=2, max_length=256)
    Description : Optional[str]  = Field(min_length=2, max_length=1024)

RoleUpdateModel.model_rebuild()
class RoleResponseModel(BaseModel):
  id          : UUID4
  RoleName    : str
  Description : str
  
RoleResponseModel.model_rebuild()
