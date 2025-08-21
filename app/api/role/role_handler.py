from app.common.utils import validate_uuid4
from app.common.database.database_interface import db_interface
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.role.role import RoleResponseModel, RoleSearchResults
from app.telemetry.tracing import trace_span

# Get the order service dynamically based on ORM type
role_service = db_interface.get_order_service()

###############################################################################

@trace_span("handler: create_role")
def create_role_(model, db_session):
    try:
        role = role_service.create_role(db_session, model)
        message = "Role created successfully"
        resp = ResponseModel[RoleResponseModel](
            Message=message, Data=role)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_role_by_id")
def get_role_by_id_(role_id, db_session):
    try:
        # role_id = validate_int(id)
        role = role_service.get_role_by_id(db_session, role_id)
        message = "Role retrieved successfully"
        resp = ResponseModel[RoleResponseModel](
            Message=message, Data=role)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_role")
def update_role_(role_id, model, db_session):
    try:
        # role_id = validate_uuid4(id)
        role = role_service.update_role(db_session, role_id, model)
        message = "Role updated successfully"
        resp = ResponseModel[RoleResponseModel](
            Message=message, Data=role)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_role")
def delete_role_(role_id, db_session):
    try:
        # role_id = validate_uuid4(id)
        role = role_service.delete_role(db_session, role_id)
        message = "Role deleted successfully"
        resp = ResponseModel[RoleResponseModel](
            Message=message, Data=role)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_roles")
def search_roles_(filter, db_session):
    try:
        roles = role_service.search_roles(db_session, filter)
        message = "Roles retrieved successfully"
        resp = ResponseModel[RoleSearchResults](Message=message, Data=roles)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

