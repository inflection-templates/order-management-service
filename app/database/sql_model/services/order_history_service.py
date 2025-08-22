import datetime as dt
from uuid import uuid4
from app.common.utils import print_colorized_json
from app.database.sql_model.models.order_history import OrderHistory
from app.domain_types.miscellaneous.exceptions import NotFound
from app.domain_types.schemas.order_history import OrderHistoryCreateModel, OrderHistoryUpdateModel, OrderHistoryResponseModel, OrderHistorySearchFilter, OrderHistorySearchResults
from sqlmodel import Session, asc, desc, select
# from sqlalchemy import desc, asc
from app.telemetry.tracing import trace_span


@trace_span("service: create_order_history")
def create_order_history(session: Session, model: OrderHistoryCreateModel) -> OrderHistoryResponseModel:
    model_dict = model.dict()
    db_model = OrderHistory(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    session.refresh(db_model)  # Refresh to ensure the database model has its final values
    order_history = db_model

    return order_history.dict()  # Use SQLModel's dict method to convert to dictionary


@trace_span("service: get_order_history_by_id")
def get_order_history_by_id(session: Session, order_history_id: str) -> OrderHistoryResponseModel:
    order_history = session.get(OrderHistory, order_history_id)  # SQLModel allows session.get for retrieving by primary key
    if not order_history:
        raise NotFound(f"Order history with id {order_history_id} not found")
    return order_history.dict()  # Convert to dictionary


@trace_span("service: update_order_history")
def update_order_history(session: Session, order_history_id: str, model: OrderHistoryUpdateModel) -> OrderHistoryResponseModel:
    order_history = session.get(OrderHistory, order_history_id)
    if not order_history:
        raise NotFound(f"Order history with id {order_history_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    
    # Using SQLModel's update function for model
    session.query(OrderHistory).filter(OrderHistory.id == order_history_id).update(update_data, synchronize_session="auto")
    session.commit()
    session.refresh(order_history)
    return order_history.dict()  # Convert to dictionary


@trace_span("service: search_order_histories")
def search_order_types(session: Session, filter: OrderHistorySearchFilter) -> OrderHistorySearchResults:
    query = session.query(OrderHistory)
    
    # Apply filters from the search filter
    if filter.OrderId:
        query = query.filter(OrderHistory.OrderId.like(f'%{filter.OrderId}%'))
    if filter.PreviousStatus:
        query = query.filter(OrderHistory.PreviousStatus.like(f'%{filter.PreviousStatus}%'))
    if filter.Status:
        query = query.filter(OrderHistory.Status.like(f'%{filter.Status}%'))
    if filter.UpdatedByUserId:
        query = query.filter(OrderHistory.UpdatedByUserId.like(f'%{filter.UpdatedByUserId}%'))
    if filter.Timestamp:
        query = query.filter(OrderHistory.Timestamp == filter.Timestamp)

    # Handle ordering
    if filter.OrderBy is None:
        filter.OrderBy = "CreatedAt"
    if not hasattr(OrderHistory, filter.OrderBy):
        filter.OrderBy = "CreatedAt"
    
    orderBy = getattr(OrderHistory, filter.OrderBy)

    # Apply ordering direction
    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    orderHistories = query.all()

    items = list(map(lambda x: x.dict(), orderHistories))  # Convert results to dictionary using dict()

    results = OrderHistorySearchResults(
        TotalCount=len(orderHistories),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results


@trace_span("service: delete_order_history")
def delete_order_history(session: Session, order_history_id: str):
    order_history = session.get(OrderHistory, order_history_id)
    if not order_history:
        raise NotFound(f"Order history with id {order_history_id} not found")
    session.delete(order_history)
    session.commit()
    return True
