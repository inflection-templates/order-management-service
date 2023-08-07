import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.order import Order, OrderStatusMachine
from app.domain_types.miscellaneous.exceptions import NotFound, HTTPError
from app.domain_types.schemas.order import OrderCreateModel, OrderResponseModel, OrderUpdateModel, OrderSearchFilter, OrderSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import cast, func, asc, desc
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
    temp = session.refresh(db_model)
    order = db_model

    return order.__dict__

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
    session.query(Order).filter(Order.id == order_id).update(update_data, synchronize_session="auto")

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

@trace_span("service: search_orders")
def search_orders(session: Session, filter: OrderSearchFilter) -> OrderSearchResults:

    query = session.query(Order)

    if filter.CustomerId:
        query = query.filter(Order.CustomerId .like(f'%{filter.CustomerId}%'))
    if filter.AssociatedCartId:
        query = query.filter(Order.AssociatedCartId.like(f'%{filter.AssociatedCartId}%'))
    if filter.TotalItemsCountGreaterThan:
        query = query.filter(Order.TotalItemsCount > filter.TotalItemsCountGreaterThan)
    if filter.TotalItemsCountLessThan:
        query = query.filter(Order.TotalItemsCount < filter.TotalItemsCountLessThan)
    if filter.OrderDiscountGreaterThan:
        query = query.filter(Order.OrderDiscount > filter.OrderDiscountGreaterThan)
    if filter.OrderDiscountLessThan:
        query = query.filter(Order.OrderDiscount < filter.OrderDiscountLessThan)
    if filter.TotalAmountGreaterThan:
        query = query.filter(Order.TotalAmount > filter.TotalAmountGreaterThan)
    if filter.TotalAmountLessThan:
        query = query.filter(Order.TotalAmount < filter.TotalAmountLessThan)
    if filter.OrderStatus:
        query = query.filter(Order.OrderStatus == filter.OrderStatus)
    if filter.OrderType:
        query = query.filter(Order.OrderType.like(f'%{filter.OrderType}%'))
    if filter.CreatedBefore:
        query = query.filter(Order.CreatedAt.date() < filter.CreatedBefore)
    if filter.CreatedAfter:
        query = query.filter(Order.CreatedAt.date() > filter.CreatedAfter)
    if filter.PastMonths:
        query = searchByPastMonths(filter.PastMonths)

    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(Order, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(Order, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    orders = query.all()

    items = list(map(lambda x: x.__dict__, orders))

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
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise NotFound(f"Order with id {order_id} not found")

    previous_state = order.OrderStatus.value
    updated_state = status.value

    # order_status = OrderStatusMachine()

    # if previous_state == "Draft" and updated_state =="Inventry Checked":
    #     status_value = "create_order"
    #     transition_method = getattr(order_status, status_value, None)
    #     if transition_method:
    #         transition_method()
    #         session.query(Order).filter(Order.id == order_id).update({Order.OrderStatus:status}, synchronize_session="auto")
    #     else:
    #         print("Invalid state transition")

    # transition_method = getattr(order_status, status_value, None)
    # if transition_method:
    #     transition_method()
    # else:
    #     print("Invalid state transition")

    if check_valid_transition(previous_state, updated_state):
        session.query(Order).filter(Order.id == order_id).update({Order.OrderStatus:status}, synchronize_session="auto")

    session.commit()
    session.refresh(order)
    return order.__dict__

def check_valid_transition(previous_state, updated_state):
    order_status = OrderStatusMachine()

    if previous_state == "Draft" and updated_state =="Inventry Checked":
        status_value = "create_order"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Inventry Checked" and updated_state == "Confirmed":
        status_value = "confirm_order"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Confirmed" and updated_state == "Payment Initiated":
        status_value = "initiate_payment"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Payment Initiated" and updated_state == "Payment Completed":
        status_value = "complete_payment"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Payment Initiated" and updated_state == "Payment Failed":
        status_value = "retry_payment"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Payment Completed" and updated_state == "Placed":
        status_value = "placed_order"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Placed" and updated_state == "Shipped":
        status_value = "shipped_order"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Shipped" and updated_state == "Delivered":
        status_value = "delivered_order"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state in ["Delivered", "Exchanged", "Refunded"] and updated_state == "Closed":
        status_value = "closed_order"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Closed" and updated_state == "Reopened":
        status_value = "reopen_order"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Reopened" and updated_state == "Return Initiated":
        status_value = "initiate_return"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Return Initiated" and updated_state == "Returned":
        status_value = "complete_return"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Returned" and updated_state == "Refund Initiated":
        status_value = "initiate_refund"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Refund Initiated" and updated_state == "Refunded":
        status_value = "completed_refund"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Reopened" and updated_state == "Exchange Initiated":
        status_value = "initiate_exchange"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    elif previous_state == "Exchange Initiated" and updated_state == "Exchanged":
        status_value = "complete_exchange"
        order_status.state = previous_state
        transition_method = getattr(order_status, status_value, None)
        if transition_method:
            transition_method()
            return True
    else:
        return {"message": "Invalid state transition"}
