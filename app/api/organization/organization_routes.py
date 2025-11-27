from fastapi import APIRouter, Depends, status
from app.database.database_accessor import get_db_session
from app.api.organization.organization_handler import (
    create_organization_,
    delete_organization_,
    get_organization_by_id_,
    get_organization_by_code_,
    search_organizations_,
    update_organization_ 
)
from app.domain_types.miscellaneous.response_model import ResponseModel, ResponseStatusTypes
from app.domain_types.schemas.organization import OrganizationCreateModel, OrganizationResponseModel, OrganizationSearchFilter, OrganizationSearchResults, OrganizationUpdateModel

##############################################################################

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[OrganizationResponseModel] | None)
async def create_organization(model: OrganizationCreateModel, db_session=Depends(get_db_session)):
    return create_organization_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrganizationSearchResults|None])
async def search_organization(
    query_params: OrganizationSearchFilter = Depends(),
    db_session = Depends(get_db_session)):
    filter = OrganizationSearchFilter(**query_params.dict())
    return search_organizations_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrganizationResponseModel] | None)
async def get_organization_by_id(id: str, db_session=Depends(get_db_session)):
    return get_organization_by_id_(id, db_session)

@router.get("/code/{code}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrganizationResponseModel] | None)
async def get_organization_by_code(code: str, db_session=Depends(get_db_session)):
    return get_organization_by_code_(code, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=OrganizationResponseModel | None)
async def update_organization(id: str, model: OrganizationUpdateModel, db_session=Depends(get_db_session)):
    return update_organization_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[OrganizationResponseModel] | None)
async def delete_organization(id: str, db_session=Depends(get_db_session)):
    return delete_organization_(id, db_session)

