import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.customer import Customer
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.customer import CustomerCreateModel, CustomerUpdateModel, CustomerResponseModel, CustomerSearchFilter, CustomerSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.telemetry.tracing import trace_span

@trace_span("service: create_customer")
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
    # print_colorized_json(customer)
    return customer.__dict__

@trace_span("service: get_customer_by_id")
def get_customer_by_id(session: Session, customer_id: str) -> CustomerResponseModel:
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise NotFound(f"Customer with id {customer_id} not found")
<<<<<<< HEAD

    # customer = CustomerResponseModel(**Customer.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
    print_colorized_json(customer)
=======
>>>>>>> origin/main
    return customer.__dict__

@trace_span("service: update_customer")
def update_customer(session: Session, customer_id: str, model: CustomerUpdateModel) -> CustomerResponseModel:
<<<<<<< HEAD
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
=======
    update_data = {}
    if model.Name != None and model.Name != "":
        update_data["Name"] = model.Name
    if model.Email != None:
        update_data["Email"] = model.Email
    if model.PhoneCode != None:
        update_data["PhoneCode"] = model.PhoneCode
    if model.Phone != None:
        update_data["Phone"] = model.Phone
    if model.TaxNumber != None:
        update_data["TaxNumber"] = model.TaxNumber
    if model.ProfilePicture != None:
        update_data["ProfilePicture"] = model.ProfilePicture

    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise NotFound(f"Customer with id {customer_id} not found")
    
    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Customer).filter(Customer.id == customer_id).update(update_data, synchronize_session="auto")

    session.commit()
    session.refresh(customer)
    return customer.__dict__

@trace_span("service: search_customers")
def search_customers(session: Session, filter) -> CustomerSearchResults:

    query = session.query(Customer)
    if filter.Name:
        query = query.filter(Customer.Name == filter.Name)
    if filter.Email:
        query = query.filter(Customer.Email == filter.Email)
    if filter.PhoneCode:
        query = query.filter(Customer.PhoneCode == filter.PhoneCode)
    if filter.Phone:
        query = query.filter(Customer.Phone == filter.Phone)
    if filter.TaxNumber:
        query = query.filter(Customer.TaxNumber == filter.TaxNumber)
    customers = query.all()

    results = CustomerSearchResults(
        TotalCount=len(customers),
        ItemsPerPage=filter.ItemsPerPage,
        PageNumber=filter.PageNumber,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=customers
    )

    return results.__dict__

@trace_span("service: delete_customer")
def delete_customer(session: Session, customer_id: str):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise NotFound(f"Customer with id {customer_id} not found")
    session.delete(customer)
    session.commit()
    return True
>>>>>>> origin/main
