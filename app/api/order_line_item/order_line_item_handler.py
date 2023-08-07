from app.common.utils import validate_uuid4
from app.database.services import order_line_item_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.order_line_item import OrderLineItemResponseModel, OrderLineItemSearchResults
from app.telemetry.tracing import trace_span

@trace_span("handler: create_order_line_item")
def create_order_line_item_(model, db_session):
    try:
        order_line_item = order_line_item_service.create_order_line_item(db_session, model)
        message = "Order line item created successfully"
        resp = ResponseModel[OrderLineItemResponseModel](Message=message, Data=order_line_item)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_order_line_item_by_id")
def get_order_line_item_by_id_(id, db_session):
    try:
        order_line_item_id = validate_uuid4(id)
        order_line_item = order_line_item_service.get_order_line_item_by_id(db_session, order_line_item_id)
        message = "Order line item retrieved successfully"
        resp = ResponseModel[OrderLineItemResponseModel](Message=message, Data=order_line_item)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_order_line_item")
def update_order_line_item_(id, model, db_session):
    try:
        order_line_item_id = validate_uuid4(id)
        order_line_item = order_line_item_service.update_order_line_item(db_session, order_line_item_id, model)
        message = "Order line item updated successfully"
        resp = ResponseModel[OrderLineItemResponseModel](Message=message, Data=order_line_item)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_order_line_item")
def delete_order_line_item_(id, db_session):
    try:
        order_line_item_id = validate_uuid4(id)
        order_line_item = order_line_item_service.delete_order_line_item(db_session, order_line_item_id)
        message = "Order line item deleted successfully"
        resp = ResponseModel[bool](Message=message, Data=order_line_item)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_order_line_items")
def search_order_line_items_(filter, db_session):
    try:
        order_line_items = order_line_item_service.search_order_line_items(db_session, filter)
        message = "Order line items retrieved successfully"
        resp = ResponseModel[OrderLineItemSearchResults](Message=message, Data=order_line_items)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()