import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.order_history import OrderHistory
from app.domain_types.miscellaneous.exceptions import NotFound
from app.domain_types.schemas.order_history import OrderHistoryCreateModel, OrderHistoryUpdateModel, OrderHistoryResponseModel, OrderHistorySearchFilter, OrderHistorySearchResults
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.telemetry.tracing import trace_span

@trace_span("service: create_order_history")
def create_order_history(session: Session, model: OrderHistoryCreateModel) -> OrderHistoryResponseModel:
    model_dict = model.dict()
    db_model = OrderHistory(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    order_history = db_model

    return order_history.__dict__

@trace_span("service: get_order_history_by_id")
def get_order_history_by_id(session: Session, order_history_id: str) -> OrderHistoryResponseModel:
    order_history = session.query(OrderHistory).filter(OrderHistory.id == order_history_id).first()
    if not order_history:
        raise NotFound(f"Order history with id {order_history_id} not found")
    return order_history.__dict__

@trace_span("service: update_order_history")
def update_order_history(session: Session, order_history_id: str, model: OrderHistoryUpdateModel) ->OrderHistoryResponseModel:
    order_history = session.query(OrderHistory).filter(OrderHistory.id == order_history_id).first()
    if not order_history:
        raise NotFound(f"Order history with id {order_history_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(OrderHistory).filter(OrderHistory.id == order_history_id).update(
        update_data, synchronize_session="auto")

    session.commit()
    session.refresh(order_history)
    return order_history.__dict__

@trace_span("service: delete_order_history")
def delete_order_history(session: Session, order_history_id: str):
    order_history = session.query(OrderHistory).filter(OrderHistory.id == order_history_id).first()
    if not order_history:
        raise NotFound(f"Order history with id {order_history_id} not found")
    session.delete(order_history)
    session.commit()
    return True

@trace_span("service: search_order_histories")
def search_order_types(session: Session, filter) -> OrderHistorySearchResults:

    query = session.query(OrderHistory)
    if filter.OrderId:
        query = query.filter(OrderHistory.OrderId == filter.OrderId)
    if filter.PreviousStatus:
        query = query.filter(OrderHistory.PreviousStatus == filter.PreviousStatus)
    if filter.Status:
        query = query.filter(OrderHistory.Status == filter.Status)
    if filter.UpdatedByUserId:
        query = query.filter(OrderHistory.UpdatedByUserId == filter.UpdatedByUserId)
    if filter.Timestamp:
        query = query.filter(OrderHistory.Timestamp == filter.Timestamp)
    order_histories = query.all()

    results = OrderHistorySearchResults(
        TotalCount=len(order_histories),
        ItemsPerPage=filter.ItemsPerPage,
        PageNumber=filter.PageNumber,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=order_histories
    )

    return results.__dict__



