from fastapi import APIRouter, Depends, status
from app.api.customer.customer_handler import (
    create_customer_,
    get_customer_by_id_,
    update_customer_,
    delete_customer_,
    search_customers_
)
from app.database.database_accessor import get_db_session
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.customer import CustomerCreateModel, CustomerSearchFilter, CustomerSearchResults, CustomerUpdateModel, CustomerResponseModel

###############################################################################

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[CustomerResponseModel|None])
async def create_customer(model: CustomerCreateModel, db_session = Depends(get_db_session)):
    return create_customer_(model, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[CustomerResponseModel|None])
async def get_customer_by_id(id: str, db_session = Depends(get_db_session)):
    return get_customer_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[CustomerResponseModel|None])
async def update_customer(id: str, model: CustomerUpdateModel, db_session = Depends(get_db_session)):
    return update_customer_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[bool])
async def delete_customer(id: str, db_session = Depends(get_db_session)):
    return delete_customer_(id, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[CustomerSearchResults|None])
async def search_customer(
        query_params: CustomerSearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = CustomerSearchFilter(**query_params.dict())
    return search_customers_(filter, db_session)
