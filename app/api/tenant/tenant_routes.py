from fastapi import APIRouter, Depends, status
from app.database.database_accessor import get_db_session
from app.api.tenant.tenant_handler import (
    create_tenant_,
    delete_tenant_,
    get_tenant_by_id_,
    get_tenant_by_code_,
    search_tenants_,
    update_tenant_ 
)
from app.domain_types.miscellaneous.response_model import ResponseModel, ResponseStatusTypes
from app.domain_types.schemas.tenant import TenantCreateModel, TenantResponseModel, TenantSearchFilter, TenantSearchResults, TenantUpdateModel

##############################################################################

router = APIRouter(
    prefix="/tenants",
    tags=["tenants"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[TenantResponseModel] | None)
async def create_tenant(model: TenantCreateModel, db_session=Depends(get_db_session)):
    return create_tenant_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[TenantSearchResults|None])
async def search_tenant(
    query_params: TenantSearchFilter = Depends(),
    db_session = Depends(get_db_session)):
    filter = TenantSearchFilter(**query_params.dict())
    return search_tenants_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[TenantResponseModel] | None)
async def get_tenant_by_id(id: str, db_session=Depends(get_db_session)):
    return get_tenant_by_id_(id, db_session)

@router.get("/code/{code}", status_code=status.HTTP_200_OK, response_model=ResponseModel[TenantResponseModel] | None)
async def get_tenant_by_code(code: str, db_session=Depends(get_db_session)):
    return get_tenant_by_code_(code, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=TenantResponseModel | None)
async def update_tenant(id: str, model: TenantUpdateModel, db_session=Depends(get_db_session)):
    return update_tenant_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[TenantResponseModel] | None)
async def delete_tenant(id: str, db_session=Depends(get_db_session)):
    return delete_tenant_(id, db_session)

