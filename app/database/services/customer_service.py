import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.customer import Customer
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.customer import CustomerCreateModel, CustomerUpdateModel, CustomerResponseModel, CustomerSearchFilter, CustomerSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import func

def create_customer(session: Session, model: CustomerCreateModel) -> CustomerResponseModel:

    customer = None

    if model.Email != None and model.Email != "":
        existing_customer = session.query(Customer).filter(
            func.lower(Customer.Email) == func.lower(model.Email)
        ).first()
        if existing_customer:
            raise Conflict(f"Customer with email {model.Email} already exists!")

    if model.Phone != None and model.Phone != "":
        existing_customer = session.query(Customer).filter(
            Customer.Phone == model.Phone
        ).first()
        if existing_customer:
            raise Conflict(f"Customer with phone {model.Phone} already exists!")

    if model.TaxNumber != None and model.TaxNumber != "":
        existing_customer = session.query(Customer).filter(
            func.lower(Customer.TaxNumber) == func.lower(model.TaxNumber)
        ).first()
        if existing_customer:
            raise Conflict(f"Customer with tax number {model.TaxNumber} already exists!")

    model_dict = model.dict()
    db_model = Customer(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    customer = db_model

    print_colorized_json(customer)

    return customer.__dict__

def get_customer_by_id(session: Session, customer_id: str) -> CustomerResponseModel:
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise NotFound(f"Customer with id {customer_id} not found")

    # customer = CustomerResponseModel(**Customer.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
    print_colorized_json(customer)
    return customer.__dict__

def update_customer(session: Session, customer_id: str, model: CustomerUpdateModel) -> CustomerResponseModel:
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise NotFound(f"Customer with id {customer_id} not found")
        
    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Customer).filter(Customer.id == customer_id).update(update_data, synchronize_session="auto")

    session.commit()
    session.refresh(customer)
    
    print_colorized_json(customer)
    return customer.__dict__

def delete_customer(session: Session, customer_id: str) -> CustomerResponseModel:
    customer = session.query(Customer).get(customer_id)
    if not customer:
        raise NotFound(f"Customer with id {customer_id} not found")
        
    session.delete(customer)

    session.commit()
       
    print_colorized_json(customer)
    return customer.__dict__
