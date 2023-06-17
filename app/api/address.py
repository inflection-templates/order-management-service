from fastapi import APIRouter, Depends, status, Query, Body
from app.common.utils import print_colorized_json, validate_uuid4
from app.database.database_accessor import get_db_session
from app.database.services import address_service
from app.domain_types.schemas.address import AddressCreateModel, AddressUpdateModel, AddressResponseModel

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
) 

@router.post("/", status_code=201, response_model=AddressResponseModel|None)
async def create_address(model: AddressCreateModel, db_session = Depends(get_db_session)):
    print_colorized_json(model)
    address = address_service.create_address(db_session, model)
    return address 

@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=AddressResponseModel|None)
async def get_address_by_id(id: str, db_session = Depends(get_db_session)):
    address_id = validate_uuid4(id)
    return address_service.get_address_by_id(db_session, address_id) 

@router.put("/{id}", status_code=200, response_model=AddressResponseModel|None)
async def update_address(id: str, model: AddressUpdateModel, db_session = Depends(get_db_session)):
    address_id = validate_uuid4(id)
    return address_service.update_address(db_session, address_id, model) 