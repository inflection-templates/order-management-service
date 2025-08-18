from fastapi import APIRouter, Depends, status, Query, Body
from app.common.utils import print_colorized_json, validate_uuid4
from app.database.database_accessor import get_db_session
from app.api.users.users_handler import (
    create_users_,
    get_users_by_id_,
    update_users_,
    delete_users_,
    search_users_
)
from app.domain_types.schemas.users import UserCreateModel, UserUpdateModel, UserResponseModel, UserSearchResults, UserSearchFilter, DeleteResponseModel
from app.domain_types.miscellaneous.response_model import ResponseModel, ResponseStatusTypes

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[UserResponseModel | None])
async def create_users(model: UserCreateModel, db_session=Depends(get_db_session)):
    return create_users_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[UserSearchResults | None])
async def search_users(
        query_params: UserSearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = UserSearchFilter(**query_params.dict())
    return search_users_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[UserResponseModel | None])
async def get_users_by_id(id: str, db_session=Depends(get_db_session)):
    return get_users_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[UserResponseModel | None])
async def update_users(id: str, model: UserUpdateModel, db_session=Depends(get_db_session)):
    return update_users_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[DeleteResponseModel | None])
async def delete_users(id: str, db_session=Depends(get_db_session)):
    return delete_users_(id, db_session)
