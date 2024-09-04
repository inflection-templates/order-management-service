from typing import Optional
from app.common.utils import validate_uuid4
from app.database.services import user_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.user import UserCreateModel, UserResponseModel, UserSearchResults
from app.telemetry.tracing import trace_span

@trace_span("handler: create_user")
def create_user_(model:UserCreateModel, db_session):
    try:
        user = user_service.create_user(db_session, model)
        message = "User created successfully"
        resp = ResponseModel[UserResponseModel](Message=message, Data=user)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_user_by_id")
def get_user_by_id_(id, db_session):
    try:
        user_id = validate_uuid4(id)
        customer = user_service.get_user_by_id(db_session, user_id)
        message = "User retrieved successfully"
        resp = ResponseModel[UserResponseModel](Message=message, Data=customer)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_user")
def update_user_(id, model, db_session):
    try:
        user_id = validate_uuid4(id)
        user = user_service.update_user(db_session, user_id, model)
        message = "User updated successfully"
        resp = ResponseModel[UserResponseModel](Message=message, Data=user)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_user")
def delete_user_(id, db_session):
    try:
        user_id = validate_uuid4(id)
        user = user_service.delete_user(db_session, user_id)
        message = "User deleted successfully"
        resp = ResponseModel[bool](Message=message, Data=user)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()    

@trace_span("handler: search_users")
def search_users_(filter, db_session):
    try:
        users = user_service.search_users(db_session, filter)
        message = "User retrieved successfully"
        resp = ResponseModel[UserSearchResults](Message=message, Data=users)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()
