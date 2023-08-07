from fastapi import APIRouter, Depends, status
from app.api.order_line_item.order_line_item_handler import (
    create_order_line_item_,
    get_order_line_item_by_id_,
    update_order_line_item_,
    delete_order_line_item_,
    search_order_line_items_
)
from app.database.database_accessor import get_db_session
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.order_line_item import OrderLineItemCreateModel, OrderLineItemResponseModel, OrderLineItemUpdateModel, OrderLineItemSearchFilter, OrderLineItemSearchResults

###############################################################################

router = APIRouter(
    prefix="/order_line_items",
    tags=["order_line_items"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[OrderLineItemResponseModel|None])
async def create_order_line_item(model: OrderLineItemCreateModel, db_session = Depends(get_db_session)):
    return  create_order_line_item_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderLineItemSearchResults|None])
async def search_order_line_items(
        query_params: OrderLineItemSearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = OrderLineItemSearchFilter(**query_params.dict())
    return search_order_line_items_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderLineItemResponseModel|None])
async def get_order_line_item_by_id(id: str, db_session = Depends(get_db_session)):
    return get_order_line_item_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderLineItemResponseModel|None])
async def update_order_line_item(id: str, model: OrderLineItemUpdateModel, db_session = Depends(get_db_session)):
    return update_order_line_item_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[bool])
async def delete_order_line_item(id: str, db_session = Depends(get_db_session)):
    return delete_order_line_item_(id, db_session)

