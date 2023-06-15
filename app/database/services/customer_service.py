import datetime as dt
import uuid
from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.database_accessor import LocalSession
from app.database.models.customer import Customer
from app.domain_types.schemas.customer import CustomerCreateModel, CustomerUpdateModel, CustomerResponseModel, CustomerSearchFilter, CustomerSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import or_

def create_customer(session: Session, model: CustomerCreateModel) -> CustomerResponseModel:

    customer = None
    try:
        existing_customer = session.query(Customer).filter(
            or_(
            Customer.Email == model.Email,
            Customer.Phone == model.Phone,
            Customer.TaxNumber == model.TaxNumber
            )).first()
        if existing_customer:
            raise HTTPException(status_code=406, detail="Customer already exists")
        
        model_dict = model.dict()
        db_model = Customer(**model_dict)
        db_model.UpdatedAt = dt.datetime.now()
        session.add(db_model)
        session.commit()
        temp = session.refresh(db_model)
        customer = db_model
    except Exception as e:
        print(e)
        session.rollback()
        raise e

    print_colorized_json(customer)
    return customer.__dict__

def get_customer_by_id(session: Session, customer_id: str) -> CustomerResponseModel:
    try:
        customer = session.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
          raise HTTPException(status_code=404, detail=f"Customer with id {customer_id} not found")
    except Exception as e:
        print(e)
        session.rollback()
        raise e
    finally:
        session.close()

    # customer = CustomerResponseModel(**Customer.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
    print_colorized_json(customer)
    return customer.__dict__ 

def update_customer(session: Session, customer_id: str, model: CustomerUpdateModel) -> CustomerResponseModel:
    try:
        # update_data = {}
        # if model.Name:
        #     update_data["Name"] = model.Name
        # if model.Email :
        #     update_data["Email"] = model.Email 
        # if model.PhoneCode:
        #     update_data["PhoneCode"] = model.PhoneCode
        # if model.Phone:
        #     update_data["Phone"] = model.Phone
        # if model.TaxNumber :
        #     update_data["TaxNumber"] = model.TaxNumber 
        # if model.ProfilePicture:
        #     update_data["ProfilePicture"] = model.ProfilePicture
        customer = session.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
          raise HTTPException(status_code=404, detail=f"Customer with id {customer_id} not found")
        
        update_data = model.dict(exclude_unset=True)
        update_data["UpdatedAt"] = dt.datetime.now()
        session.query(Customer).filter(Customer.id == customer_id).update(update_data, synchronize_session="auto")

        session.commit()
        session.refresh(customer)
    except Exception as e:
        print(e)
        session.rollback()
        raise e
    finally:
        session.close()

    # customer = CustomerResponseModel(**Customer.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
    print_colorized_json(customer)
    return customer.__dict__ 

# def search_customer(session: Session, filter: str = Query(None)) -> CustomerSearchResults:
#     try:
#         query = session.query(Customer)
#         if filter.Name:
#           query = query.filter(Customer.Name == filter.Name)
#         if filter.Email:
#           query = query.filter(Customer.Email == filter.Email)
#         if filter.PhoneCode:
#           query = query.filter(Customer.PhoneCode == filter.PhoneCode)
#         if filter.Phone:
#           query = query.filter(Customer.Phone == filter.Phone)
#         if filter.TaxNumber:
#           query = query.filter(Customer.TaxNumber == filter.TaxNumber)
#         customers = query.all()
    
#     except Exception as e:
#         print(e)
#         session.rollback()
#         raise e
#     finally:
#         session.close()

#     # customer = CustomerResponseModel(**Customer.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
#     print_colorized_json(customers)
#     return customers.__dict__