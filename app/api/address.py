from fastapi import APIRouter, Depends, status, Query, Body
from app.common.utils import print_colorized_json, validate_uuid4
from app.database.database_accessor import get_db_session
from app.database.services import address_service
from app.domain_types.schemas.address import AddressCreateModel, AddressUpdateModel, AddressResponseModel 
from app.domain_types.miscellaneous.response_model import ResponseModel, ResponseStatusTypes

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
) 

@router.post("/", status_code=201, response_model=ResponseModel[AddressResponseModel]|None)
async def create_address(model: AddressCreateModel, db_session = Depends(get_db_session)):
    try:
        print_colorized_json(model)
        address = address_service.create_address(db_session, model)
        message = "Address created successfully"
        resp = ResponseModel[AddressResponseModel](Message=message, Data=address)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close() 

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[AddressResponseModel]|None)
async def get_address_by_id(id: str, db_session = Depends(get_db_session)):
    try: 
        address_id = validate_uuid4(id)
        address = address_service.get_address_by_id(db_session, address_id) 
        message = "Address retrieved successfully"
        resp = ResponseModel[AddressResponseModel](Message=message, Data=address)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=AddressResponseModel|None)
async def update_address(id: str, model: AddressUpdateModel, db_session = Depends(get_db_session)):
    try:
        address_id = validate_uuid4(id)
        address = address_service.update_address(db_session, address_id, model) 
        message = "Address updated successfully"
        resp = ResponseModel[AddressResponseModel](Message=message, Data=address)
        # logger.info(resp)
        return resp 
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close() 

@router.delete("/{id}", status_code=200, response_model=ResponseModel[AddressResponseModel]|None)
async def delete_address(id: str, db_session = Depends(get_db_session)):
    try:
        customer_id = validate_uuid4(id)
        customer = address_service.delete_address(db_session, customer_id) 
        message = "Address deleted successfully"
        resp = ResponseModel[AddressResponseModel](Message=message, Data=customer)
        # logger.info(resp)
        return resp
    except Exception as e:
            print(e)
            db_session.rollback()
            raise e
    finally:
            db_session.close()