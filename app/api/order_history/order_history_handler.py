from app.common.utils import validate_uuid4
from app.database.services import order_history_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.order_history import OrderHistoryResponseModel, OrderHistorySearchResults
from app.telemetry.tracing import trace_span

@trace_span("handler: create_order_history")
def create_order_history_(model, db_session):
    try:
        order_history = order_history_service.create_order_history(db_session, model)
        message = "Order history created successfully"
        resp = ResponseModel[OrderHistoryResponseModel](Message=message, Data=order_history)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_order_history_by_id")
def get_order_history_by_id_(id, db_session):
    try:
        order_history_id = validate_uuid4(id)
        order_history = order_history_service.get_order_history_by_id(db_session, order_history_id)
        message = "Order history retrieved successfully"
        resp = ResponseModel[OrderHistoryResponseModel](Message=message, Data=order_history)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_order_history")
def update_order_history_(id, model, db_session):
    try:
        order_history_id = validate_uuid4(id)
        order_history = order_history_service.update_order_history(db_session, order_history_id, model)
        message = "Order history updated successfully"
        resp = ResponseModel[OrderHistoryResponseModel](Message=message, Data=order_history)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_order_histories")
def search_order_histories_(filter, db_session):
    try:
        order_histories = order_history_service.search_order_histories(db_session, filter)
        message = "Order histories retrieved successfully"
        resp = ResponseModel[OrderHistorySearchResults](Message=message, Data=order_histories)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_order_history")
def delete_order_history_(id, db_session):
    try:
        order_history_id = validate_uuid4(id)
        order_history = order_history_service.delete_order_history(db_session, order_history_id)
        message = "Order history deleted successfully"
        resp = ResponseModel[bool](Message=message, Data=order_history)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()


