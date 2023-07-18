from fastapi import APIRouter, Depends, status, Query, Body
from app.common.utils import print_colorized_json, validate_uuid4
from app.database.database_accessor import get_db_session
from app.api.address.address_handler import (
    create_address_,
    get_address_by_id_,
    update_address_,
    delete_address_,
    search_addresses_
)
from app.domain_types.schemas.address import AddressCreateModel, AddressUpdateModel, AddressResponseModel, AddressSearchResults, AddressSearchFilter
from app.domain_types.miscellaneous.response_model import ResponseModel, ResponseStatusTypes

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[AddressResponseModel] | None)
async def create_address(model: AddressCreateModel, db_session=Depends(get_db_session)):
    return create_address_(model, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[AddressResponseModel] | None)
async def get_address_by_id(id: str, db_session=Depends(get_db_session)):
    return get_address_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=AddressResponseModel | None)
async def update_address(id: str, model: AddressUpdateModel, db_session=Depends(get_db_session)):
    return update_address_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[AddressResponseModel] | None)
async def delete_address(id: str, db_session=Depends(get_db_session)):
    return delete_address(id, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[AddressSearchResults | None])
async def search_customer(
        query_params: AddressSearchFilter = Depends(),
        db_session=Depends(get_db_session)):
    filter = AddressSearchFilter(**query_params.dict())
    return search_addresses_(filter, db_session)
