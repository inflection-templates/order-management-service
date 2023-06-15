import uuid
from fastapi import APIRouter, Depends, status, Query, Body
from app.common.logger import logger
from app.common.utils import print_colorized_json, validate_uuid4
from app.database.database_accessor import get_db_session
from app.database.services import customer_service
from app.domain_types.schemas.customer import CustomerCreateModel, CustomerUpdateModel, CustomerResponseModel, CustomerSearchFilter, CustomerSearchResults
from app.domain_types.schemas.order import OrderCreateModel, OrderResponseModel
from app.domain_types.miscellaneous.response_model import ResponseModel, ResponseStatusTypes

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[CustomerResponseModel]|None)
async def create_customer(model: CustomerCreateModel, db_session = Depends(get_db_session)):
    try:
        print_colorized_json(model)
        customer = customer_service.create_customer(db_session, model)
        message = "Customer created successfully"
        resp = ResponseModel[CustomerResponseModel](Message=message, Data=customer)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=CustomerResponseModel|None)
async def get_customer_by_id(id: str, db_session = Depends(get_db_session)):
    try:
        customer_id = validate_uuid4(id)
        return customer_service.get_customer_by_id(db_session, customer_id)
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@router.put("/{id}", status_code=200, response_model=CustomerResponseModel|None)
async def update_customer(id: str, model: CustomerUpdateModel, db_session = Depends(get_db_session)):
    customer_id = validate_uuid4(id)
    return customer_service.update_customer(db_session, customer_id, model)

# @router.get("/search", status_code=status.HTTP_302_FOUND, response_model=CustomerSearchResults|None)
# async def search_customer(filter: str = Query(None), db_session = Depends(get_db_session)):

#     return customer_service.search_customer(db_session, filter)
