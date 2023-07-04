from fastapi import APIRouter, Depends, status
from app.api.order_history.order_history_handler import (
    create_order_history_,
    get_order_history_by_id_,
    update_order_history_,
    delete_order_history_,
    search_order_histories_
)
from app.database.database_accessor import get_db_session
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.order_history import OrderHistoryCreateModel, OrderHistoryResponseModel, OrderHistoryUpdateModel, OrderHistorySearchResults, OrderHistorySearchFilter

###############################################################################

router = APIRouter(
    prefix="/order_histories",
    tags=["order_histories"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[OrderHistoryResponseModel|None])
async def create_order_history(model: OrderHistoryCreateModel, db_session = Depends(get_db_session)):
    return  create_order_history_(model, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderHistoryResponseModel|None])
async def get_order_historyby_id(id: str, db_session = Depends(get_db_session)):
    return get_order_history_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderHistoryResponseModel|None])
async def update_order_history(id: str, model: OrderHistoryUpdateModel, db_session = Depends(get_db_session)):
    return update_order_history_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[bool])
async def delete_order_history(id: str, db_session = Depends(get_db_session)):
    return delete_order_history_(id, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderHistorySearchResults|None])
async def search_order_histories(
        query_params: OrderHistorySearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = OrderHistorySearchFilter(**query_params.dict())
    return search_order_histories_(filter, db_session)