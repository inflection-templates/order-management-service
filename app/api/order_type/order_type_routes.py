from fastapi import APIRouter, Depends, status
from app.api.order_type.order_type_handler import (
    create_order_type_,
    get_order_type_by_id_,
    update_order_type_,
    delete_order_type_,
    search_order_types_
)
from app.database.database_accessor import get_db_session
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.order_type import OrderTypeCreateModel, OrderTypeResponseModel, OrderTypeUpdateModel, OrderTypeSearchFilter, OrderTypeSearchResults

###############################################################################

router = APIRouter(
    prefix="/order_types",
    tags=["order_types"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[OrderTypeResponseModel|None])
async def create_order_type(model: OrderTypeCreateModel, db_session = Depends(get_db_session)):
    return  create_order_type_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderTypeSearchResults|None])
async def search_order_types(
        query_params: OrderTypeSearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = OrderTypeSearchFilter(**query_params.dict())
    return search_order_types_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderTypeResponseModel|None])
async def get_order_type_by_id(id: str, db_session = Depends(get_db_session)):
    return get_order_type_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderTypeResponseModel|None])
async def update_order_type(id: str, model: OrderTypeUpdateModel, db_session = Depends(get_db_session)):
    return update_order_type_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[bool])
async def delete_order_type(id: str, db_session = Depends(get_db_session)):
    return delete_order_type_(id, db_session)
