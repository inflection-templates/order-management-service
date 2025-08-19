from typing import Optional
from app.common.utils import validate_uuid4
from app.database_alchemy.services import api_client_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.api_client import ApiClientCreateModel, ApiClientResponseModel, ApiClientSearchResults
from app.telemetry.tracing import trace_span

@trace_span("handler: create_api_client")
def create_api_client_(model:ApiClientCreateModel, db_session):
    try:
        
        api_client = api_client_service.create_api_client(db_session, model)
        message = "Api client created successfully"
        resp = ResponseModel[ApiClientResponseModel](Message=message, Data=api_client)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_api_client_by_id")
def get_api_client_by_id_(id, db_session):
    try:
        api_client_id = validate_uuid4(id)
        customer = api_client_service.get_api_client_by_id(db_session, api_client_id)
        message = "Api client retrieved successfully"
        resp = ResponseModel[ApiClientResponseModel](Message=message, Data=customer)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_api_client")
def update_api_client_(id, model, db_session):
    try:
        api_client_id = validate_uuid4(id)
        api_client = api_client_service.update_api_client(db_session, api_client_id, model)
        message = "Api client updated successfully"
        resp = ResponseModel[ApiClientResponseModel](Message=message, Data=api_client)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_api_client")
def delete_api_client_(id, db_session):
    try:
        api_client_id = validate_uuid4(id)
        api_client = api_client_service.delete_api_client(db_session, api_client_id)
        message = "Api client deleted successfully"
        resp = ResponseModel[bool](Message=message, Data=api_client)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()    

@trace_span("handler: search_api_clients")
def search_api_clients_(filter, db_session):
    try:
        api_clients = api_client_service.search_api_clients(db_session, filter)
        message = "Api clients retrieved successfully"
        resp = ResponseModel[ApiClientSearchResults](Message=message, Data=api_clients)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()
