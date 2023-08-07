import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.order_line_item import OrderLineItem
from app.domain_types.miscellaneous.exceptions import NotFound
from app.domain_types.schemas.order_line_item import OrderLineItemCreateModel, OrderLineItemResponseModel, OrderLineItemUpdateModel,OrderLineItemSearchFilter,OrderLineItemSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from app.telemetry.tracing import trace_span

@trace_span("service: create_order_line_item")
def create_order_line_item(session: Session, model: OrderLineItemCreateModel) -> OrderLineItemResponseModel:
    model_dict = model.dict()
    db_model = OrderLineItem(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    order_line_item = db_model

    return order_line_item.__dict__

@trace_span("service: get_order_line_item_by_id")
def get_order_line_item_by_id(session: Session, order_line_item_id: str) -> OrderLineItemResponseModel:
    order_line_item = session.query(OrderLineItem).filter(OrderLineItem.id == order_line_item_id).first()
    if not order_line_item:
        raise NotFound(f"Order line item with id {order_line_item_id} not found")
    return order_line_item.__dict__

@trace_span("service: update_order_line_item")
def update_order_line_item(session: Session, order_line_item_id: str, model: OrderLineItemUpdateModel) -> OrderLineItemResponseModel:
    order_line_item = session.query(OrderLineItem).filter(OrderLineItem.id == order_line_item_id).first()
    if not order_line_item:
        raise NotFound(f"Order line item with id {order_line_item_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(OrderLineItem).filter(OrderLineItem.id == order_line_item_id).update(
        update_data, synchronize_session="auto")

    session.commit()
    session.refresh(order_line_item)
    return order_line_item.__dict__

@trace_span("service: delete_order_line_item")
def delete_order_line_item(session: Session, order_line_item_id: str):
    order_line_item = session.query(OrderLineItem).filter(OrderLineItem.id == order_line_item_id).first()
    if not order_line_item:
        raise NotFound(f"Order line item with id {order_line_item_id} not found")
    session.delete(order_line_item)
    session.commit()
    return True

@trace_span("service: search_order_line_items")
def search_order_line_items(session: Session, filter: OrderLineItemSearchFilter) -> OrderLineItemSearchResults:

    query = session.query(OrderLineItem)

    if filter.Name:
        query = query.filter(OrderLineItem.Name.like(f'%{filter.Name}%'))
    if filter.CatalogId:
        query = query.filter(OrderLineItem.CatalogId.like(f'%{filter.CatalogId}%'))
    if filter.DiscountSchemeId:
        query = query.filter(OrderLineItem.DiscountSchemeId.like(f'%{filter.DiscountSchemeId}%'))
    if filter.OrderId:
        query = query.filter(OrderLineItem.OrderId.like(f'%{filter.OrderId}%'))
    if filter.CartId:
        query = query.filter(OrderLineItem.CartId.like(f'%{filter.CartId}%'))
    if filter.ItemSubTotal:
        query = query.filter(OrderLineItem.ItemSubTotal == filter.ItemSubTotal)
    if filter.CreatedBefore:
        query = query.filter(OrderLineItem.CreatedAt < filter.CreatedBefore)
    if filter.CreatedAfter:
        query = query.filter(OrderLineItem.CreatedAt > filter.CreatedAfter)

    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(OrderLineItem, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(OrderLineItem, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    orderLineItems = query.all()

    items = list(map(lambda x: x.__dict__, orderLineItems))

    results = OrderLineItemSearchResults(
        TotalCount=len(orderLineItems),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results