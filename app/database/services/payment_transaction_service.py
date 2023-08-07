import datetime as dt
import uuid
from app.common.utils import print_colorized_json
from app.database.models.payment_transaction import PaymentTransaction
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.payment_transaction import PaymentTransactionCreateModel, PaymentTransactionResponseModel, PaymentTransactionSearchFilter, PaymentTransactionSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from app.telemetry.tracing import trace_span

@trace_span("service: create_payment_transaction")
def create_payment_transaction(session: Session, model: PaymentTransactionCreateModel) -> PaymentTransactionResponseModel:
    model_dict = model.dict()
    db_model = PaymentTransaction(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    payment_transaction = db_model

    return payment_transaction.__dict__

@trace_span("service: get_payment_transaction_by_id")
def get_payment_transaction_by_id(session: Session, payment_transaction_id: str) -> PaymentTransactionResponseModel:
    payment_transaction = session.query(PaymentTransaction).filter(PaymentTransaction.id == payment_transaction_id).first()
    if not payment_transaction:
        raise NotFound(f"payment_transaction with id {payment_transaction_id} not found")
    return payment_transaction.__dict__

@trace_span("service: delete_payment_transaction")
def delete_payment_transaction(session: Session, payment_transaction_id: str):
    payment_transaction = session.query(PaymentTransaction).filter(PaymentTransaction.id == payment_transaction_id).first()
    if not payment_transaction:
        raise NotFound(f"payment_transaction with id {payment_transaction_id} not found")
    session.delete(payment_transaction)
    session.commit()
    return True

@trace_span("service: search_payment_transactions")
def search_payment_transactions(session: Session, filter: PaymentTransactionSearchFilter) -> PaymentTransactionSearchResults:

    query = session.query(PaymentTransaction)

    if filter.DisplayCode:
        query = query.filter(PaymentTransaction.DisplayCode.like(f'%{filter.DisplayCode}%'))
    if filter.InvoiceNumber:
        query = query.filter(PaymentTransaction.InvoiceNumber == filter.InvoiceNumber)
    if filter.BankTransactionId:
        query = query.filter(PaymentTransaction.BankTransactionId == filter.BankTransactionId)
    if filter.CustomerId:
        query = query.filter(PaymentTransaction.CustomerId.like(f'%{filter.CustomerId}%'))
    if filter.OrderId:
        query = query.filter(PaymentTransaction.OrderId.like(f'%{filter.OrderId}%'))
    if filter.PaymentMode:
        query = query.filter(PaymentTransaction.PaymentMode.like(f'%{filter.PaymentMode}%'))
    if filter.PaymentAmount:
        query = query.filter(PaymentTransaction.PaymentAmount.like(f'%{filter.PaymentAmount}%'))
    if filter.IsRefund:
        query = query.filter(PaymentTransaction.IsRefund == filter.IsRefund)
    if filter.InitiatedDate:
        query = query.filter(PaymentTransaction.InitiatedDate == filter.InitiatedDate)

    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(PaymentTransaction, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(PaymentTransaction, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    paymentTransactions = query.all()

    items = list(map(lambda x: x.__dict__, paymentTransactions))

    results = PaymentTransactionSearchResults(
        TotalCount=len(paymentTransactions),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results