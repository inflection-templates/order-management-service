from fastapi import APIRouter, Depends, status
from app.api.order.order_handler import (
    create_order_,
    get_order_by_id_,
    update_order_,
    delete_order_,
    search_orders_,
    update_order_status_
)
from app.database.database_accessor import get_db_session
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.order import OrderCreateModel, OrderResponseModel, OrderUpdateModel, OrderSearchFilter, OrderSearchResults
from app.domain_types.enums.order_status_types import OrderStatusTypes

###############################################################################

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[OrderResponseModel|None])
async def create_order(model: OrderCreateModel, db_session = Depends(get_db_session)):
    return create_order_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderSearchResults|None])
async def search_order(
        query_params: OrderSearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = OrderSearchFilter(**query_params.dict())
    return search_orders_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderResponseModel|None])
async def get_order_by_id(id: str, db_session = Depends(get_db_session)):
    return get_order_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderResponseModel|None])
async def update_order(id: str, model: OrderUpdateModel, db_session = Depends(get_db_session)):
    return update_order_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[bool])
async def delete_order(id: str, db_session = Depends(get_db_session)):
    return delete_order_(id, db_session)

@router.put("/{id}/status", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderResponseModel|None])
async def update_order_status(id: str, status: OrderStatusTypes, db_session = Depends(get_db_session)):
    return update_order_status_(id, status, db_session)