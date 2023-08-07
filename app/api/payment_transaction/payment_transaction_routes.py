from fastapi import APIRouter, Depends, status
from app.api.payment_transaction.payment_transaction_handler import (
    create_payment_transaction_,
    get_payment_transaction_by_id_,
    # update_payment_transaction_,
    delete_payment_transaction_,
    search_payment_transactions_
)
from app.database.database_accessor import get_db_session
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.payment_transaction import PaymentTransactionCreateModel, PaymentTransactionResponseModel, PaymentTransactionSearchFilter, PaymentTransactionSearchResults

###############################################################################

router = APIRouter(
    prefix="/payment_transactions",
    tags=["payment_transactions"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[PaymentTransactionResponseModel|None])
async def create_payment_transaction(model: PaymentTransactionCreateModel, db_session = Depends(get_db_session)):
    return create_payment_transaction_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[PaymentTransactionSearchResults|None])
async def search_payment_transactions(
        query_params: PaymentTransactionSearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = PaymentTransactionSearchFilter(**query_params.dict())
    return search_payment_transactions_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[PaymentTransactionResponseModel|None])
async def get_payment_transaction_by_id(id: str, db_session = Depends(get_db_session)):
    return get_payment_transaction_by_id_(id, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[bool])
async def delete_payment_transaction(id: str, db_session = Depends(get_db_session)):
    return delete_payment_transaction_(id, db_session)



