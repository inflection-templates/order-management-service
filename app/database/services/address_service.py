import datetime as dt
import uuid
from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.database_accessor import LocalSession
from app.database.models.address import Address
from app.database.models.customer_address import CustomerAddress
from app.domain_types.schemas.address import AddressCreateModel, AddressResponseModel, AddressUpdateModel
from sqlalchemy.orm import Session
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound


def create_address(session: Session, model: AddressCreateModel) -> AddressResponseModel:
    model_dict = model.dict()
    db_model = Address(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    address = db_model

    # if address.CreatedBy != "None" and address.CreatedBy != "":
    #     CustomerAddress.AddressId = address.id
    #     CustomerAddress.CustomerId = address.CreatedBy

    print_colorized_json(address)
    return address.__dict__


def get_address_by_id(session: Session, address_id: str) -> AddressResponseModel:
    address = session.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise NotFound(f"Address with id {address_id} not found")

    print_colorized_json(address)

    # print_colorized_json(address)
    return address.__dict__


def get_address_by_id(session: Session, address_id: str) -> AddressResponseModel:
    try:
        address = session.query(Address).filter(
            Address.id == address_id).first()
        if not address:
            raise HTTPException(
                status_code=404, detail=f"Address with id {address_id} not found")
    except Exception as e:
        print(e)
        session.rollback()
        raise e
    finally:
        session.close()

    # customer = CustomerResponseModel(**Customer.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
    # print_colorized_json(address)

    return address.__dict__


def update_address(session: Session, address_id: str, model: AddressUpdateModel) -> AddressResponseModel:
    address = session.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise NotFound(f"Address with id {address_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Address).filter(Address.id == address_id).update(
        update_data, synchronize_session="auto")

    session.commit()
    session.refresh(address)

    print_colorized_json(address)
    return address.__dict__


def delete_address(session: Session, address_id: str) -> AddressResponseModel:
    address = session.query(Address).get(address_id)
    if not address:
        raise NotFound(f"Address with id {address_id} not found")

    session.delete(address)

    session.commit()

    print_colorized_json(address)
    return address.__dict__
