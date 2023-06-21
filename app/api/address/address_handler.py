from app.common.utils import validate_uuid4
from app.database.services import address_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.address import AddressResponseModel
from app.telemetry.tracing import trace_span

@trace_span("handler: create_address")
def create_address_(model, db_session):
    try:
        address = address_service.create_address(db_session, model)
        message = "Address created successfully"
        resp = ResponseModel[AddressResponseModel](
            Message=message, Data=address)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_address_by_id")
def get_address_by_id_(id, db_session):
    try:
        address_id = validate_uuid4(id)
        address = address_service.get_address_by_id(db_session, address_id)
        message = "Address retrieved successfully"
        resp = ResponseModel[AddressResponseModel](
            Message=message, Data=address)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_address")
def update_address_(id, model, db_session):
    try:
        address_id = validate_uuid4(id)
        address = address_service.update_address(db_session, address_id, model)
        message = "Address updated successfully"
        resp = ResponseModel[AddressResponseModel](
            Message=message, Data=address)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_address")
def delete_address_(id, db_session):
    try:
        customer_id = validate_uuid4(id)
        customer = address_service.delete_address(db_session, customer_id)
        message = "Address deleted successfully"
        resp = ResponseModel[AddressResponseModel](
            Message=message, Data=customer)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_addresses")
def search_addresses_(filter, db_session):
    try:
        addresses = address_service.search_addresses(db_session, filter)
        message = "Addresses retrieved successfully"
        resp = ResponseModel[AddressResponseModel](
            Message=message, Data=addresses)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()
