from app.common.utils import validate_uuid4
from app.database.services import merchant_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.merchant import MerchantResponseModel, MerchantSearchResults
from app.telemetry.tracing import trace_span

@trace_span("handler: create_merchant")
def create_merchant_(model, db_session):
    try:
        merchant = merchant_service.create_merchant(db_session, model)
        message = "Merchant created successfully"
        resp = ResponseModel[MerchantResponseModel](Message=message, Data=merchant)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_merchant_by_id")
def get_merchant_by_id_(id, db_session):
    try:
        merchant_id = validate_uuid4(id)
        merchant = merchant_service.get_merchant_by_id(db_session, merchant_id)
        message = "Merchant retrieved successfully"
        resp = ResponseModel[MerchantResponseModel](Message=message, Data=merchant)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_merchant")
def update_merchant_(id, model, db_session):
    try:
        merchant_id = validate_uuid4(id)
        merchant = merchant_service.update_merchant(db_session, merchant_id, model)
        message = "Merchant updated successfully"
        resp = ResponseModel[MerchantResponseModel](Message=message, Data=merchant)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_merchant")
def delete_merchant_(id, db_session):
    try:
        merchant_id = validate_uuid4(id)
        merchant = merchant_service.delete_merchant(db_session, merchant_id)
        message = "Merchant deleted successfully"
        resp = ResponseModel[bool](Message=message, Data=merchant)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_merchants")
def search_merchants_(filter, db_session):
    try:
        merchants = merchant_service.search_merchants(db_session, filter)
        message = "Merchants retrieved successfully"
        resp = ResponseModel[MerchantSearchResults](Message=message, Data=merchants)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()
