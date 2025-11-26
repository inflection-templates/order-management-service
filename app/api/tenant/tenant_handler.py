from app.common.utils import validate_uuid4
from app.database.services import tenant_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.tenant import TenantResponseModel, TenantSearchResults
from app.telemetry.tracing import trace_span

###############################################################################

@trace_span("handler: create_tenant")
def create_tenant_(model, db_session):
    try:
        tenant = tenant_service.create_tenant(db_session, model)
        message = "Tenant created successfully"
        resp = ResponseModel[TenantResponseModel](
            Message=message, Data=tenant)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_tenant_by_id")
def get_tenant_by_id_(tenant_id, db_session):
    try:
        tenant_id = validate_uuid4(tenant_id)
        tenant = tenant_service.get_tenant_by_id(db_session, tenant_id)
        message = "Tenant retrieved successfully"
        resp = ResponseModel[TenantResponseModel](
            Message=message, Data=tenant)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_tenant")
def update_tenant_(tenant_id, model, db_session):
    try:
        tenant_id = validate_uuid4(tenant_id)
        tenant = tenant_service.update_tenant(db_session, tenant_id, model)
        message = "Tenant updated successfully"
        resp = ResponseModel[TenantResponseModel](
            Message=message, Data=tenant)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_tenant")
def delete_tenant_(tenant_id, db_session):
    try:
        tenant_id = validate_uuid4(tenant_id)
        tenant_service.delete_tenant(db_session, tenant_id)
        message = "Tenant deleted successfully"
        resp = ResponseModel(
            Message=message, Data=None)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_tenants")
def search_tenants_(filter, db_session):
    try:
        tenants = tenant_service.search_tenants(db_session, filter)
        message = "Tenants retrieved successfully"
        resp = ResponseModel[TenantSearchResults](Message=message, Data=tenants)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_tenant_by_code")
def get_tenant_by_code_(code, db_session):
    try:
        tenant = tenant_service.get_tenant_by_code(db_session, code)
        message = "Tenant retrieved successfully"
        resp = ResponseModel[TenantResponseModel](
            Message=message, Data=tenant)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

