from fastapi import APIRouter, Depends, status
from app.common.database.database_interface import db_interface
from app.api.role.role_handler import (
 create_role_,
 delete_role_,
 get_role_by_id_,
 search_roles_,
 update_role_ 
)
from app.domain_types.miscellaneous.response_model import ResponseModel, ResponseStatusTypes
from app.domain_types.schemas.role.role import RoleCreateModel, RoleResponseModel, RoleSearchFilter, RoleSearchResults, RoleUpdateModel

# Get the database session function dynamically based on ORM type
get_db_session = db_interface.get_db_session()

##############################################################################

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[RoleResponseModel] | None)
async def create_role(model: RoleCreateModel, db_session=Depends(get_db_session)):
    return create_role_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[RoleSearchResults|None])
async def search_role(
    query_params: RoleSearchFilter = Depends(),
    db_session = Depends(get_db_session)):
    filter = RoleSearchFilter(**query_params.dict())
    return search_roles_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[RoleResponseModel] | None)
async def get_role_by_id(id: int, db_session=Depends(get_db_session)):
    return get_role_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=RoleResponseModel | None)
async def update_role(id: int, model: RoleUpdateModel, db_session=Depends(get_db_session)):
    return update_role_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[RoleResponseModel] | None)
async def delete_role(id: int, db_session=Depends(get_db_session)):
    return delete_role_(id, db_session)

