from app.common.utils import validate_uuid4
from app.database.services import payment_transaction_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.payment_transaction import PaymentTransactionResponseModel
from app.telemetry.tracing import trace_span

@trace_span("handler: create_payment_transaction")
def create_payment_transaction_(model, db_session):
    try:
        payment_transaction = payment_transaction_service.create_payment_transaction(db_session, model)
        message = "Payment transaction created successfully"
        resp = ResponseModel[PaymentTransactionResponseModel](Message=message, Data=payment_transaction)
        # print_colorized_json(model)
        return resp

    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_payment_transaction_by_id")
def get_payment_transaction_by_id_(id, db_session):
    try:
        payment_transaction_id = validate_uuid4(id)
        payment_transaction = payment_transaction_service.get_payment_transaction_by_id(db_session, payment_transaction_id)
        message = "Payment transaction retrieved successfully"
        resp = ResponseModel[PaymentTransactionResponseModel](Message=message, Data=payment_transaction)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_payment_transaction")
def delete_payment_transaction_(id, db_session):
    try:
        payment_transaction_id = validate_uuid4(id)
        payment_transaction = payment_transaction_service.delete_payment_transaction(db_session, payment_transaction_id)
        message = "Payment transaction deleted successfully"
        resp = ResponseModel[bool](Message=message, Data=payment_transaction)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_payment_transactions")
def search_payment_transactions_(filter, db_session):
    try:
        payment_transactions = payment_transaction_service.search_payment_transactions(db_session, filter)
        message = "Payment transactions retrieved successfully"
        resp = ResponseModel[PaymentTransactionResponseModel](Message=message, Data=payment_transactions)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()