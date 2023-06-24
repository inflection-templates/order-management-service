import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.order import Order
from app.domain_types.miscellaneous.exceptions import NotFound
from app.domain_types.schemas.order import OrderCreateModel, OrderResponseModel, OrderUpdateModel, OrderSearchFilter, OrderSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.telemetry.tracing import trace_span

@trace_span("service: create_order")
def create_order(session: Session, model: OrderCreateModel) -> OrderResponseModel:
    order = session.add(model)
    session.commit()
    session.refresh(model)
    return order

@trace_span("service: get_order_by_id")
def get_order_by_id(session: Session, order_id: str) -> OrderResponseModel:
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise NotFound(f"Order with id {order_id} not found")
    return order.__dict__

@trace_span("service: update_order")
def update_order(session: Session, order_id: str, model: OrderUpdateModel) -> OrderResponseModel:
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise NotFound(f"Order with id {order_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Order).filter(Order.id == order_id).update(
        update_data, synchronize_session="auto")

    session.commit()
    session.refresh(order)
    return order.__dict__

@trace_span("service: delete_order")
def delete_order(session: Session, order_id: str) -> OrderResponseModel:
    order = session.query(Order).get(order_id)
    if not order:
        raise NotFound(f"Order with id {order_id} not found")
    session.delete(order)
    session.commit()
    return True

