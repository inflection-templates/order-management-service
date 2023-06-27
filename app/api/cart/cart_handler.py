from app.common.utils import validate_uuid4
from app.database.services import cart_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.cart import CartResponseModel
from app.telemetry.tracing import trace_span

@trace_span("handler: create_cart")
def create_cart_(model, db_session):
    try:
        cart = cart_service.create_cart(db_session, model)
        message = "Cart created successfully"
        resp = ResponseModel[CartResponseModel](Message=message, Data=cart)
        # print_colorized_json(model)
        return resp

    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_cart_by_id")
def get_cart_by_id_(id, db_session):
    try:
        cart_id = validate_uuid4(id)
        cart = cart_service.get_cart_by_id(db_session, cart_id)
        message = "Cart retrieved successfully"
        resp = ResponseModel[CartResponseModel](Message=message, Data=cart)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_cart")
def update_cart_(id, model, db_session):
    try:
        cart_id = validate_uuid4(id)
        cart = cart_service.update_cart(db_session, cart_id, model)
        message = "Cart updated successfully"
        resp = ResponseModel[CartResponseModel](Message=message, Data=cart)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_cart")
def delete_cart_(id, db_session):
    try:
        cart_id = validate_uuid4(id)
        cart = cart_service.delete_cart(db_session, cart_id)
        message = "Cart deleted successfully"
        resp = ResponseModel[bool](Message=message, Data=cart)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_carts")
def search_carts_(filter, db_session):
    try:
        carts = cart_service.search_carts(db_session, filter)
        message = "Carts retrieved successfully"
        resp = ResponseModel[CartResponseModel](Message=message, Data=carts)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()
