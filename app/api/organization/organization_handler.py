from app.common.utils import validate_uuid4
from app.database.services import organization_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.organization import OrganizationResponseModel, OrganizationSearchResults
from app.telemetry.tracing import trace_span

###############################################################################

@trace_span("handler: create_organization")
def create_organization_(model, db_session):
    try:
        organization = organization_service.create_organization(db_session, model)
        message = "Organization created successfully"
        resp = ResponseModel[OrganizationResponseModel](
            Message=message, Data=organization)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_organization_by_id")
def get_organization_by_id_(organization_id, db_session):
    try:
        organization_id = validate_uuid4(organization_id)
        organization = organization_service.get_organization_by_id(db_session, organization_id)
        message = "Organization retrieved successfully"
        resp = ResponseModel[OrganizationResponseModel](
            Message=message, Data=organization)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_organization")
def update_organization_(organization_id, model, db_session):
    try:
        organization_id = validate_uuid4(organization_id)
        organization = organization_service.update_organization(db_session, organization_id, model)
        message = "Organization updated successfully"
        resp = ResponseModel[OrganizationResponseModel](
            Message=message, Data=organization)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_organization")
def delete_organization_(organization_id, db_session):
    try:
        organization_id = validate_uuid4(organization_id)
        organization_service.delete_organization(db_session, organization_id)
        message = "Organization deleted successfully"
        resp = ResponseModel(
            Message=message, Data=None)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_organizations")
def search_organizations_(filter, db_session):
    try:
        organizations = organization_service.search_organizations(db_session, filter)
        message = "Organizations retrieved successfully"
        resp = ResponseModel[OrganizationSearchResults](Message=message, Data=organizations)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_organization_by_code")
def get_organization_by_code_(code, db_session):
    try:
        organization = organization_service.get_organization_by_code(db_session, code)
        message = "Organization retrieved successfully"
        resp = ResponseModel[OrganizationResponseModel](
            Message=message, Data=organization)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

