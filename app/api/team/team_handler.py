from app.common.utils import validate_uuid4
from app.database.services import team_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.team import TeamResponseModel, TeamSearchResults
from app.telemetry.tracing import trace_span

###############################################################################

@trace_span("handler: create_team")
def create_team_(model, db_session):
    try:
        team = team_service.create_team(db_session, model)
        message = "Team created successfully"
        resp = ResponseModel[TeamResponseModel](
            Message=message, Data=team)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_team_by_id")
def get_team_by_id_(team_id, db_session):
    try:
        team_id = validate_uuid4(team_id)
        team = team_service.get_team_by_id(db_session, team_id)
        message = "Team retrieved successfully"
        resp = ResponseModel[TeamResponseModel](
            Message=message, Data=team)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_team")
def update_team_(team_id, model, db_session):
    try:
        team_id = validate_uuid4(team_id)
        team = team_service.update_team(db_session, team_id, model)
        message = "Team updated successfully"
        resp = ResponseModel[TeamResponseModel](
            Message=message, Data=team)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_team")
def delete_team_(team_id, db_session):
    try:
        team_id = validate_uuid4(team_id)
        team_service.delete_team(db_session, team_id)
        message = "Team deleted successfully"
        resp = ResponseModel(
            Message=message, Data=None)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_teams")
def search_teams_(filter, db_session):
    try:
        teams = team_service.search_teams(db_session, filter)
        message = "Teams retrieved successfully"
        resp = ResponseModel[TeamSearchResults](Message=message, Data=teams)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_team_by_code")
def get_team_by_code_(code, db_session):
    try:
        team = team_service.get_team_by_code(db_session, code)
        message = "Team retrieved successfully"
        resp = ResponseModel[TeamResponseModel](
            Message=message, Data=team)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

