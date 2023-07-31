from fastapi import APIRouter, Depends, status
from app.api.merchant.merchant_handler import (
    create_merchant_,
    get_merchant_by_id_,
    update_merchant_,
    delete_merchant_,
    search_merchants_
)
from app.database.database_accessor import get_db_session
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.merchant import MerchantCreateModel, MerchantUpdateModel, MerchantSearchFilter, MerchantSearchResults, MerchantResponseModel

###############################################################################

router = APIRouter(
    prefix="/merchants",
    tags=["merchants"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[MerchantResponseModel|None])
async def create_merchant(model: MerchantCreateModel, db_session = Depends(get_db_session)):
    return  create_merchant_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[MerchantSearchResults|None])
async def search_merchant(
        query_params: MerchantSearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = MerchantSearchFilter(**query_params.dict())
    return search_merchants_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[MerchantResponseModel|None])
async def get_merchant_by_id(id: str, db_session = Depends(get_db_session)):
    return get_merchant_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[MerchantResponseModel|None])
async def update_merchant(id: str, model: MerchantUpdateModel, db_session = Depends(get_db_session)):
    return update_merchant_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[bool])
async def delete_merchant(id: str, db_session = Depends(get_db_session)):
    return delete_merchant_(id, db_session)


