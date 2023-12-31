import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.order_type import OrderType
from app.domain_types.miscellaneous.exceptions import NotFound
from app.domain_types.schemas.order_type import OrderTypeCreateModel, OrderTypeResponseModel, OrderTypeUpdateModel, OrderTypeSearchFilter, OrderTypeSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from app.telemetry.tracing import trace_span

@trace_span("service: create_order_type")
def create_order_type(session: Session, model: OrderTypeCreateModel) -> OrderTypeResponseModel:
    model_dict = model.dict()
    db_model = OrderType(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    order_type = db_model

    return order_type.__dict__

@trace_span("service: get_order_type_by_id")
def get_order_type_by_id(session: Session, order_type_id: str) -> OrderTypeResponseModel:
    order_type = session.query(OrderType).filter(OrderType.id == order_type_id).first()
    if not order_type:
        raise NotFound(f"Order type with id {order_type_id} not found")
    return order_type.__dict__

@trace_span("service: update_order_type")
def update_order_type(session: Session, order_type_id: str, model: OrderTypeUpdateModel) -> OrderTypeResponseModel:
    order_type = session.query(OrderType).filter(OrderType.id == order_type_id).first()
    if not order_type:
        raise NotFound(f"Order type with id {order_type_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(OrderType).filter(OrderType.id == order_type_id).update(
        update_data, synchronize_session="auto")

    session.commit()
    session.refresh(order_type)
    return order_type.__dict__

@trace_span("service: delete_order_type")
def delete_order_type(session: Session, order_type_id: str):
    order_type = session.query(OrderType).filter(OrderType.id == order_type_id).first()
    if not order_type:
        raise NotFound(f"Order type with id {order_type_id} not found")
    session.delete(order_type)
    session.commit()
    return True

@trace_span("service: search_order_types")
def search_order_types(session: Session, filter: OrderTypeSearchFilter) -> OrderTypeSearchResults:

    query = session.query(OrderType)

    if filter.Name:
        query = query.filter(OrderType.Name.like(f'%{filter.Name}%'))
    if filter.Description:
        query = query.filter(OrderType.Description.like(f'%{filter.Description}%'))

    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(OrderType, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(OrderType, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    orderTypes = query.all()

    items = list(map(lambda x: x.__dict__, orderTypes))

    results = OrderTypeSearchResults(
        TotalCount=len(orderTypes),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results