from app.common.utils import validate_uuid4
from app.database.services import order_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.order import OrderResponseModel
from app.telemetry.tracing import trace_span


@trace_span("handler: create_order")
def create_order_(model, db_session):
    try:
        order= order_service.create_order(db_session, model)
        message = "Order created successfully"
        resp = ResponseModel[OrderResponseModel](Message=message, Data=order)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_order_by_id")
def get_order_by_id_(id, db_session):
    try:
        order_id = validate_uuid4(id)
        order= order_service.get_order_by_id(db_session, order_id)
        message = "Order retrieved successfully"
        resp = ResponseModel[OrderResponseModel](Message=message, Data=order)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_order")
def update_order_(id, model, db_session):
    try:
        order_id = validate_uuid4(id)
        order= order_service.update_order(db_session, order_id, model)
        message = "Order updated successfully"
        resp = ResponseModel[OrderResponseModel](Message=message, Data=order)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_order")
def delete_order_(id, db_session):
    try:
        order_id = validate_uuid4(id)
        order= order_service.delete_order(db_session, order_id)
        message = "Order deleted successfully"
        resp = ResponseModel[bool](Message=message, Data=order)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_orders")
def search_orders_(filter, db_session):
    try:
        orders = order_service.search_orders(db_session, filter)
        message = "Orders retrieved successfully"
        resp = ResponseModel[OrderResponseModel](Message=message, Data=orders)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_order_status")
def update_order_status_(id, status, db_session):
    try:
        order_id = validate_uuid4(id)
        order= order_service.update_order_status(db_session, order_id, status)
        message = "Order status updated successfully"
        resp = ResponseModel[OrderResponseModel](Message=message, Data=order)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()
