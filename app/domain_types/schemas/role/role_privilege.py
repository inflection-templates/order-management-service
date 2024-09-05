from pydantic import UUID4, BaseModel

class RolePrivilegeResponseModel(BaseModel):
    id        : str
    RoleId    : int
    RoleName  : str
    Privilege : str
    Scope     : str
    Enabled   : bool

