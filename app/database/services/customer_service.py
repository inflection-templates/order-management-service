import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.customer import Customer
from app.database.models.customer_address import CustomerAddress
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.customer import CustomerCreateModel, CustomerUpdateModel, CustomerResponseModel, CustomerSearchFilter, CustomerSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from app.telemetry.tracing import trace_span
from app.domain_types.schemas.customer_address import CustomerAddressCreateModel

@trace_span("service: create_customer")
def create_customer(session: Session, model: CustomerCreateModel) -> CustomerResponseModel:
    customer = None

    if model.Email != None and model.Email != "":
        existing_customer = session.query(Customer).filter(func.lower(Customer.Email) == func.lower(model.Email)).first()
        if existing_customer:
            raise Conflict(f"Customer with email {model.Email} already exists!")

    if model.Phone != None and model.Phone != "":
        existing_customer = session.query(Customer).filter(Customer.Phone == model.Phone).first()
        if existing_customer:
            raise Conflict(f"Customer with phone {model.Phone} already exists!")

    if model.TaxNumber != None and model.TaxNumber != "":
        existing_customer = session.query(Customer).filter(
            func.lower(Customer.TaxNumber) == func.lower(model.TaxNumber)).first()
        if existing_customer:
            raise Conflict(f"Customer with tax number {model.TaxNumber} already exists!")

    model_dict = model.dict()
    db_model = Customer(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    customer = db_model

    if model.DefaultShippingAddressId != None and model.DefaultShippingAddressId != "" :
        customer_address = add_customer_address(session, customer.id, customer.DefaultShippingAddressId, "Shipping")

    if model.DefaultBillingAddressId != model.DefaultShippingAddressId :
        customer_address = add_customer_address(session, customer.id, customer.DefaultBillingAddressId, "Billing")

    return customer.__dict__

def add_customer_address(session, customer_id, address_id, address_type):
    customer_address = CustomerAddress(
            CustomerId = customer_id,
            AddressId = address_id,
            AddressType = address_type,
            IsFavorite = True
        )
    session.add(customer_address)
    session.commit()
    return customer_address

@trace_span("service: get_customer_by_id")
def get_customer_by_id(session: Session, customer_id: str) -> CustomerResponseModel:
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise NotFound(f"Customer with id {customer_id} not found")
    return customer.__dict__

@trace_span("service: update_customer")
def update_customer(session: Session, customer_id: str, model: CustomerUpdateModel) -> CustomerResponseModel:
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise NotFound(f"Customer with id {customer_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Customer).filter(Customer.id == customer_id).update(
        update_data, synchronize_session="auto")

    session.commit()
    session.refresh(customer)
    return customer.__dict__

@trace_span("service: search_customers")
def search_customers(session: Session, filter: CustomerSearchFilter) -> CustomerSearchResults:

    query = session.query(Customer)

    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(Customer, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(Customer, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    if filter.Name:
        query = query.filter(Customer.Name.like(f'%{filter.Name}%'))
    if filter.Email:
        query = query.filter(Customer.Email.like(f'%{filter.Email}%'))
    if filter.PhoneCode:
        query = query.filter(Customer.PhoneCode == filter.PhoneCode)
    if filter.Phone:
        query = query.filter(Customer.Phone.like(f'%{filter.Phone}%'))
    if filter.TaxNumber:
        query = query.filter(Customer.TaxNumber.like(f'%{filter.TaxNumber}%'))
    customers = query.all()

    items = list(map(lambda x: x.__dict__, customers))

    results = CustomerSearchResults(
        TotalCount=len(customers),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results

@trace_span("service: delete_customer")
def delete_customer(session: Session, customer_id: str):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise NotFound(f"Customer with id {customer_id} not found")
    session.delete(customer)
    session.commit()
    return True
