from app.common.utils import validate_uuid4
from app.database.services import order_type_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.order_type import OrderTypeResponseModel, OrderTypeSearchResults
from app.telemetry.tracing import trace_span

@trace_span("handler: create_order_type")
def create_order_type_(model, db_session):
    try:
        order_type = order_type_service.create_order_type(db_session, model)
        message = "Order type created successfully"
        resp = ResponseModel[OrderTypeResponseModel](Message=message, Data=order_type)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_order_type_by_id")
def get_order_type_by_id_(id, db_session):
    try:
        order_type_id = validate_uuid4(id)
        order_type = order_type_service.get_order_type_by_id(db_session, order_type_id)
        message = "Order type retrieved successfully"
        resp = ResponseModel[OrderTypeResponseModel](Message=message, Data=order_type)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_order_type")
def update_order_type_(id, model, db_session):
    try:
        order_type_id = validate_uuid4(id)
        order_type = order_type_service.update_order_type(db_session, order_type_id, model)
        message = "Order type updated successfully"
        resp = ResponseModel[OrderTypeResponseModel](Message=message, Data=order_type)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_order_type")
def delete_order_type_(id, db_session):
    try:
        order_type_id = validate_uuid4(id)
        order_type = order_type_service.delete_order_type(db_session, order_type_id)
        message = "Order type deleted successfully"
        resp = ResponseModel[bool](Message=message, Data=order_type)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_order_types")
def search_order_types_(filter, db_session):
    try:
        order_types = order_type_service.search_order_types(db_session, filter)
        message = "Order types retrieved successfully"
        resp = ResponseModel[OrderTypeSearchResults](Message=message, Data=order_types)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()




