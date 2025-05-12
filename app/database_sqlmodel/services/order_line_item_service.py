import datetime as dt
from app.common.utils import print_colorized_json
from app.database.models.order_line_item import OrderLineItem
from app.domain_types.miscellaneous.exceptions import NotFound
from app.domain_types.schemas.order_line_item import OrderLineItemCreateModel, OrderLineItemResponseModel, OrderLineItemUpdateModel, OrderLineItemSearchFilter, OrderLineItemSearchResults
from sqlmodel import Session, asc, desc, select, update
from app.telemetry.tracing import trace_span

@trace_span("service: create_order_line_item")
def create_order_line_item(session: Session, model: OrderLineItemCreateModel) -> OrderLineItemResponseModel:
    model_dict = model.dict()
    db_model = OrderLineItem(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    
    # Return response model
    return db_model.dict()

@trace_span("service: get_order_line_item_by_id")
def get_order_line_item_by_id(session: Session, order_line_item_id: str) -> OrderLineItemResponseModel:
    query = select(OrderLineItem).where(OrderLineItem.id == order_line_item_id)
    order_line_item = session.exec(query).first()
    if not order_line_item:
        raise NotFound(f"Order line item with id {order_line_item_id} not found")
    return order_line_item.dict()

@trace_span("service: update_order_line_item")
def update_order_line_item(session: Session, order_line_item_id: str, model: OrderLineItemUpdateModel) -> OrderLineItemResponseModel:
    query = select(OrderLineItem).where(OrderLineItem.id == order_line_item_id)
    order_line_item = session.exec(query).first()
    if not order_line_item:
        raise NotFound(f"Order line item with id {order_line_item_id} not found")
    
    # Updating model values
    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()

    stmt = update(OrderLineItem).where(OrderLineItem.id == order_line_item_id).values(update_data)
    session.exec(stmt)
    session.commit()

    # Return the updated model
    session.refresh(order_line_item)
    return order_line_item.dict()

@trace_span("service: delete_order_line_item")
def delete_order_line_item(session: Session, order_line_item_id: str):
    query = select(OrderLineItem).where(OrderLineItem.id == order_line_item_id)
    order_line_item = session.exec(query).first()
    if not order_line_item:
        raise NotFound(f"Order line item with id {order_line_item_id} not found")
    session.delete(order_line_item)
    session.commit()
    return True

@trace_span("service: search_order_line_items")
def search_order_line_items(session: Session, filter: OrderLineItemSearchFilter) -> OrderLineItemSearchResults:
    query = select(OrderLineItem)

    if filter.Name:
        query = query.where(OrderLineItem.Name.like(f'%{filter.Name}%'))
    if filter.CatalogId:
        query = query.where(OrderLineItem.CatalogId.like(f'%{filter.CatalogId}%'))
    if filter.DiscountSchemeId:
        query = query.where(OrderLineItem.DiscountSchemeId.like(f'%{filter.DiscountSchemeId}%'))
    if filter.OrderId:
        query = query.where(OrderLineItem.OrderId.like(f'%{filter.OrderId}%'))
    if filter.CartId:
        query = query.where(OrderLineItem.CartId.like(f'%{filter.CartId}%'))
    if filter.ItemSubTotal:
        query = query.where(OrderLineItem.ItemSubTotal == filter.ItemSubTotal)
    if filter.CreatedBefore:
        query = query.where(OrderLineItem.CreatedAt < filter.CreatedBefore)
    if filter.CreatedAfter:
        query = query.where(OrderLineItem.CreatedAt > filter.CreatedAfter)

    if filter.OrderBy is None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(OrderLineItem, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    order_by = getattr(OrderLineItem, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(order_by))
    else:
        query = query.order_by(asc(order_by))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    order_line_items = session.exec(query).all()

    items = list(map(lambda x: x.dict(), order_line_items))

    results = OrderLineItemSearchResults(
        TotalCount=len(order_line_items),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results
