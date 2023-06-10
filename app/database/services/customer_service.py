import datetime as dt
import uuid
from app.common.utils import print_colorized_json
from app.database.database_accessor import LocalSession
from app.database.models.customer import Customer
from app.domain_types.schemas.customer import CustomerCreateModel, CustomerResponseModel
from sqlalchemy.orm import Session

def create_customer(session: Session, model: CustomerCreateModel) -> CustomerResponseModel:

    customer = None
    try:
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

# def get_customer_by_id(session: Session, customer_id: str) -> CustomerResponseModel:
#     try:
#         customer = session.db.f(model)
#         session.db.commit()
#         session.db.refresh(model)
#     except Exception as e:
#         print(e)
#         session.db.rollback()
#         raise e
#     finally:
#         session.db.close()

#     # customer = CustomerResponseModel(**model.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
#     print_colorized_json(customer)
#     return customer