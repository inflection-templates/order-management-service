from fastapi import APIRouter, Depends, status, Request
from app.api.order.order_handler import (
    create_order_,
    get_order_by_id_,
    update_order_,
    delete_order_,
    search_orders_,
    update_order_status_
)
from app.database.database_interface import db_interface
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.order import OrderCreateModel, OrderResponseModel, OrderUpdateModel, OrderSearchFilter, OrderSearchResults
from app.domain_types.enums.order_status_types import OrderStatusTypes
from app.auth import authenticate_user, AuthContext

# Get the database session function dynamically based on ORM type
get_db_session = db_interface.get_db_session()

###############################################################################

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[OrderResponseModel|None])
@authenticate_user(required=True)  # Require authentication to create orders
async def create_order(
    model: OrderCreateModel,
    request: Request,
    db_session = Depends(get_db_session),  # This will automatically use the configured ORM
    **kwargs
):
    auth_context = kwargs.get('auth_context')
    return create_order_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderSearchResults|None])
@authenticate_user(required=True)  # Require authentication to search orders
async def search_order(
    query_params: OrderSearchFilter = Depends(),
    request: Request = None,
    db_session = Depends(get_db_session),
    **kwargs
):
    auth_context = kwargs.get('auth_context')
    filter = OrderSearchFilter(**query_params.dict())
    return search_orders_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderResponseModel|None])
@authenticate_user(required=True)  # Require authentication to get order details
async def get_order_by_id(
    id: str,
    request: Request,
    db_session = Depends(get_db_session),
    **kwargs
):
    auth_context = kwargs.get('auth_context')
    return get_order_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderResponseModel|None])
@authenticate_user(required=True, roles=["admin", "manager"])  # Only admins and managers can update orders
async def update_order(
    id: str,
    model: OrderUpdateModel,
    request: Request,
    db_session = Depends(get_db_session),
    **kwargs
):
    auth_context = kwargs.get('auth_context')
    return update_order_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[bool])
@authenticate_user(required=True, roles=["admin"])  # Only admins can delete orders
async def delete_order(
    id: str,
    request: Request,
    db_session = Depends(get_db_session),
    **kwargs
):
    auth_context = kwargs.get('auth_context')
    return delete_order_(id, db_session)

@router.put("/{id}/status", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrderResponseModel|None])
@authenticate_user(required=True, roles=["admin", "manager", "staff"])  # Staff can update order status
async def update_order_status(
    id: str,
    status: OrderStatusTypes,
    request: Request,
    db_session = Depends(get_db_session),
    **kwargs
):
    auth_context = kwargs.get('auth_context')
    return update_order_status_(id, status, db_session)
