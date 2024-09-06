from pydantic import UUID4, BaseModel
class PersonRoleResponseModel(BaseModel):
  id          : UUID4
  PersonId    : str
  RoleId      : str
  RoleName    : str
  
PersonRoleResponseModel.model_rebuild()
 