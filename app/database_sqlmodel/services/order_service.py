import datetime as dt
import uuid
from app.common.utils import print_colorized_json
from app.database.models.order import Order, OrderStatusMachine
from app.domain_types.miscellaneous.exceptions import NotFound, HTTPError
from app.domain_types.schemas.order import OrderCreateModel, OrderResponseModel, OrderUpdateModel, OrderSearchFilter, OrderSearchResults
from sqlmodel import Session, select, update, asc, desc
from app.telemetry.tracing import trace_span
from app.domain_types.enums.order_status_types import OrderStatusTypes
from datetime import timedelta


@trace_span("service: create_order")
def create_order(session: Session, model: OrderCreateModel) -> OrderResponseModel:
    model_dict = model.dict()
    db_model = Order(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    order = db_model
    return order.dict()


@trace_span("service: get_order_by_id")
def get_order_by_id(session: Session, order_id: str) -> OrderResponseModel:
    query = select(Order).where(Order.id == order_id)
    order = session.exec(query).first()
    if not order:
        raise NotFound(f"Order with id {order_id} not found")
    return order.dict()


@trace_span("service: update_order")
def update_order(session: Session, order_id: str, model: OrderUpdateModel) -> OrderResponseModel:
    query = select(Order).where(Order.id == order_id)
    order = session.exec(query).first()
    if not order:
        raise NotFound(f"Order with id {order_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()

    stmt = update(Order).where(Order.id == order_id).values(update_data)
    session.exec(stmt)
    session.commit()

    session.refresh(order)
    return order.dict()


@trace_span("service: delete_order")
def delete_order(session: Session, order_id: str) -> bool:
    query = select(Order).where(Order.id == order_id)
    order = session.exec(query).first()
    if not order:
        raise NotFound(f"Order with id {order_id} not found")
    session.delete(order)
    session.commit()
    return True


@trace_span("service: search_orders")
def search_orders(session: Session, filter: OrderSearchFilter) -> OrderSearchResults:
    query = select(Order)

    if filter.CustomerId:
        query = query.where(Order.CustomerId.like(f'%{filter.CustomerId}%'))
    if filter.AssociatedCartId:
        query = query.where(Order.AssociatedCartId.like(f'%{filter.AssociatedCartId}%'))
    if filter.TotalItemsCountGreaterThan:
        query = query.where(Order.TotalItemsCount > filter.TotalItemsCountGreaterThan)
    if filter.TotalItemsCountLessThan:
        query = query.where(Order.TotalItemsCount < filter.TotalItemsCountLessThan)
    if filter.OrderDiscountGreaterThan:
        query = query.where(Order.OrderDiscount > filter.OrderDiscountGreaterThan)
    if filter.OrderDiscountLessThan:
        query = query.where(Order.OrderDiscount < filter.OrderDiscountLessThan)
    if filter.TotalAmountGreaterThan:
        query = query.where(Order.TotalAmount > filter.TotalAmountGreaterThan)
    if filter.TotalAmountLessThan:
        query = query.where(Order.TotalAmount < filter.TotalAmountLessThan)
    if filter.OrderStatus:
        query = query.where(Order.OrderStatus == filter.OrderStatus)
    if filter.OrderType:
        query = query.where(Order.OrderType.like(f'%{filter.OrderType}%'))
    if filter.CreatedBefore:
        query = query.where(Order.CreatedAt < filter.CreatedBefore)
    if filter.CreatedAfter:
        query = query.where(Order.CreatedAt > filter.CreatedAfter)
    if filter.PastMonths:
        query = searchByPastMonths(filter.PastMonths)

    if filter.OrderBy is None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(Order, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    order_by = getattr(Order, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(order_by))
    else:
        query = query.order_by(asc(order_by))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    orders = session.exec(query).all()

    items = [order.dict() for order in orders]

    results = OrderSearchResults(
        TotalCount=len(orders),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results


def searchByPastMonths(pastMonths):
    date = dt.date.today()
    past_date = date - timedelta(days=pastMonths * 30)
    order_date = str(Order.CreatedAt.date())
    if order_date >= past_date:
        return Order


@trace_span("service: update_order_status")
def update_order_status(session: Session, order_id: str, status: OrderStatusTypes) -> OrderResponseModel:
    query = select(Order).where(Order.id == order_id)
    order = session.exec(query).first()
    if not order:
        raise NotFound(f"Order with id {order_id} not found")

    previous_state = order.OrderStatus.value
    updated_state = status.value

    if check_valid_transition(previous_state, updated_state):
        stmt = update(Order).where(Order.id == order_id).values({Order.OrderStatus:status})
        session.exec(stmt)
        session.commit()

    session.refresh(order)
    return order.dict()


def check_valid_transition(previous_state, updated_state):
    order_status = OrderStatusMachine()

    state_transitions = {
        ("Draft", "Inventry Checked"): "create_order",
        ("Inventry Checked", "Confirmed"): "confirm_order",
        ("Confirmed", "Payment Initiated"): "initiate_payment",
        ("Payment Initiated", "Payment Completed"): "complete_payment",
        ("Payment Initiated", "Payment Failed"): "retry_payment",
        ("Payment Completed", "Placed"): "placed_order",
        ("Placed", "Shipped"): "shipped_order",
        ("Shipped", "Delivered"): "delivered_order",
        ("Delivered", "Exchanged"): "closed_order",
        ("Refunded", "Closed"): "closed_order",
        ("Closed", "Reopened"): "reopen_order",
        ("Reopened", "Return Initiated"): "initiate_return",
        ("Return Initiated", "Returned"): "complete_return",
    }

    transition_key = (previous_state, updated_state)
    if transition_key in state_transitions:
        transition_method = getattr(order_status, state_transitions[transition_key], None)
        if transition_method:
            transition_method()
            return True
    return False
