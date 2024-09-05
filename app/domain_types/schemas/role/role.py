from pydantic import UUID4, BaseModel, Field

class RoleCreateModel(BaseModel):
  RoleName    : str = Field(description='Name of the user role')
  Description : str = Field(description='Description of user role')

class RoleResponseModel(BaseModel):
  id          : UUID4
  RoleName    : str
  Description : str
