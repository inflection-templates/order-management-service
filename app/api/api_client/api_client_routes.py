from fastapi import APIRouter, Depends, status
from app.api.api_client.api_client_handler import (
    create_api_client_,
    get_api_client_by_id_,
    update_api_client_,
    delete_api_client_,
    search_api_clients_
)
from app.database.database_interface import db_interface
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.api_client import ApiClientCreateModel, ApiClientsSearchFilter, ApiClientSearchResults, ApiClientUpdateModel, ApiClientResponseModel

# Get the database session function dynamically based on ORM type
get_db_session = db_interface.get_db_session()

###############################################################################

router = APIRouter(
    prefix="/api_clients",
    tags=["api_clients"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[ApiClientResponseModel|None])
async def create_api_client(model: ApiClientCreateModel, db_session = Depends(get_db_session)):
    return create_api_client_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[ApiClientSearchResults|None])
async def search_api_clients(
        query_params: ApiClientsSearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = ApiClientsSearchFilter(**query_params.dict())
    return search_api_clients_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[ApiClientResponseModel|None])
async def get_api_client_by_id(id: str, db_session = Depends(get_db_session)):
    return get_api_client_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[ApiClientResponseModel|None])
async def update_api_client(id: str, model: ApiClientUpdateModel, db_session = Depends(get_db_session)):
    return update_api_client_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[bool])
async def delete_api_client(id: str, db_session = Depends(get_db_session)):
    return delete_api_client_(id, db_session)
