from fastapi import APIRouter, Depends, status
from app.database.database_accessor import get_db_session
from app.api.team.team_handler import (
    create_team_,
    delete_team_,
    get_team_by_id_,
    get_team_by_code_,
    search_teams_,
    update_team_ 
)
from app.domain_types.miscellaneous.response_model import ResponseModel, ResponseStatusTypes
from app.domain_types.schemas.team import TeamCreateModel, TeamResponseModel, TeamSearchFilter, TeamSearchResults, TeamUpdateModel

##############################################################################

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[TeamResponseModel] | None)
async def create_team(model: TeamCreateModel, db_session=Depends(get_db_session)):
    return create_team_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[TeamSearchResults|None])
async def search_team(
    query_params: TeamSearchFilter = Depends(),
    db_session = Depends(get_db_session)):
    filter = TeamSearchFilter(**query_params.dict())
    return search_teams_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[TeamResponseModel] | None)
async def get_team_by_id(id: str, db_session=Depends(get_db_session)):
    return get_team_by_id_(id, db_session)

@router.get("/code/{code}", status_code=status.HTTP_200_OK, response_model=ResponseModel[TeamResponseModel] | None)
async def get_team_by_code(code: str, db_session=Depends(get_db_session)):
    return get_team_by_code_(code, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=TeamResponseModel | None)
async def update_team(id: str, model: TeamUpdateModel, db_session=Depends(get_db_session)):
    return update_team_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[TeamResponseModel] | None)
async def delete_team(id: str, db_session=Depends(get_db_session)):
    return delete_team_(id, db_session)

