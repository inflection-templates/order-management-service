from fastapi import APIRouter, Depends, status, Query, Body
from app.common.auth_decorators import authenticate_admin, authenticate_user
from app.common.utils import print_colorized_json, validate_uuid4
from app.database.database_accessor import get_db_session
from app.api.address.address_handler import (
    create_address_,
    get_address_by_id_,
    update_address_,
    delete_address_,
    search_addresses_
)
from app.domain_types.schemas.auth import TokenData
from app.domain_types.schemas.address import AddressCreateModel, AddressUpdateModel, AddressResponseModel, AddressSearchResults, AddressSearchFilter
from app.domain_types.schemas.users import DeleteResponseModel
from app.domain_types.miscellaneous.response_model import ResponseModel, ResponseStatusTypes

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[AddressResponseModel | None])
@authenticate_admin
async def create_address(
    model: AddressCreateModel, 
    db_session=Depends(get_db_session),
    current_user: TokenData = None  # This will be set by the decorator
):
    """Create a new address - requires admin role"""
    # The decorator ensures only admins can access this endpoint
    # current_user is available if you need it, but handler doesn't need it
    return create_address_(model, db_session)


@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[AddressSearchResults | None])
@authenticate_user
async def search_address(
    query_params: AddressSearchFilter = Depends(),
    db_session=Depends(get_db_session),
    current_user: TokenData = None
):
    """Search addresses - requires user or admin role"""
    filter = AddressSearchFilter(**query_params.dict())
    return search_addresses_(filter, db_session)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[AddressResponseModel | None])
@authenticate_user
async def get_address_by_id(
    id: str, 
    db_session=Depends(get_db_session),
    current_user: TokenData = None
):
    """Get address by ID - requires user or admin role"""
    validate_uuid4(id)
    return get_address_by_id_(id, db_session)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[AddressResponseModel | None])
@authenticate_admin
async def update_address(
    id: str, 
    model: AddressUpdateModel, 
    db_session=Depends(get_db_session),
    # current_user: TokenData = None
):
    """Update address - requires admin role"""
    validate_uuid4(id)
    return update_address_(id, model, db_session)


@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[DeleteResponseModel | None])
@authenticate_admin
async def delete_address(
    id: str, 
    db_session=Depends(get_db_session),
    # current_user: TokenData = None
):
    """Delete address - requires admin role"""
    validate_uuid4(id)
    return delete_address_(id, db_session)

