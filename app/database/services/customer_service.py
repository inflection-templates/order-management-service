import uuid
from app.common.utils import print_colorized_json
from app.database.database_accessor import DatabaseSession
from app.domain_types.schemas.customer import CustomerCreateModel, CustomerResponseModel


def create_customer(db_session: DatabaseSession, model: CustomerCreateModel) -> CustomerResponseModel:
    try:
        customer = db_session.db.add(model)
        db_session.db.commit()
        db_session.db.refresh(model)
    except Exception as e:
        print(e)
        db_session.db.rollback()
        raise e
    finally:
        db_session.db.close()

    # customer = CustomerResponseModel(**model.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
    print_colorized_json(customer)
    return customer

# def get_customer_by_id(db_session: DatabaseSession, customer_id: str) -> CustomerResponseModel:
#     try:
#         customer = db_session.db.f(model)
#         db_session.db.commit()
#         db_session.db.refresh(model)
#     except Exception as e:
#         print(e)
#         db_session.db.rollback()
#         raise e
#     finally:
#         db_session.db.close()

#     # customer = CustomerResponseModel(**model.dict(), id=uuid.uuid4(), DisplayCode="1234", InvoiceNumber="1234")
#     print_colorized_json(customer)
#     return customer