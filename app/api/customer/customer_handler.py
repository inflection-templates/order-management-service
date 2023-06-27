from app.common.utils import validate_uuid4
from app.database.services import customer_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.customer import CustomerResponseModel
from app.telemetry.tracing import trace_span

@trace_span("handler: create_customer")
def create_customer_(model, db_session):
    try:
        customer = customer_service.create_customer(db_session, model)
        message = "Customer created successfully"
        resp = ResponseModel[CustomerResponseModel](Message=message, Data=customer)
        # print_colorized_json(model)
        return resp

    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_customer_by_id")
def get_customer_by_id_(id, db_session):
    try:
        customer_id = validate_uuid4(id)
        customer = customer_service.get_customer_by_id(db_session, customer_id)
        message = "Customer retrieved successfully"
        resp = ResponseModel[CustomerResponseModel](Message=message, Data=customer)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: update_customer")
def update_customer_(id, model, db_session):
    try:
        customer_id = validate_uuid4(id)
        customer = customer_service.update_customer(db_session, customer_id, model)
        message = "Customer updated successfully"
        resp = ResponseModel[CustomerResponseModel](Message=message, Data=customer)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_customer")
def delete_customer_(id, db_session):
    try:
        customer_id = validate_uuid4(id)
        customer = customer_service.delete_customer(db_session, customer_id)
        message = "Customer deleted successfully"
        resp = ResponseModel[bool](Message=message, Data=customer)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_customers")
def search_customers_(filter, db_session):
    try:
        customers = customer_service.search_customers(db_session, filter)
        message = "Customers retrieved successfully"
        resp = ResponseModel[CustomerResponseModel](Message=message, Data=customers)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()
