import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.merchant import Merchant
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.merchant import MerchantCreateModel, MerchantUpdateModel, MerchantSearchFilter, MerchantResponseModel, MerchantSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.telemetry.tracing import trace_span

@trace_span("service: create_Merchant")
def create_merchant(session: Session, model: MerchantCreateModel) -> MerchantResponseModel:
    merchant = None

    if model.Email != None and model.Email != "":
        existing_merchant = session.query(Merchant).filter(func.lower(Merchant.Email) == func.lower(model.Email)).first()
        if existing_merchant:
            raise Conflict(f"Merchant with email {model.Email} already exists!")

    if model.Phone != None and model.Phone != "":
        existing_merchant = session.query(Merchant).filter(Merchant.Phone == model.Phone).first()
        if existing_merchant:
            raise Conflict(f"Merchant with phone {model.Phone} already exists!")

    if model.TaxNumber != None and model.TaxNumber != "":
        existing_merchant = session.query(Merchant).filter(
            func.lower(Merchant.TaxNumber) == func.lower(model.TaxNumber)).first()
        if existing_merchant:
            raise Conflict(f"Merchant with tax number {model.TaxNumber} already exists!")

    if model.GSTNumber != None and model.GSTNumber != "":
        existing_merchant = session.query(Merchant).filter(
            func.lower(Merchant.GSTNumber) == func.lower(model.GSTNumber)).first()
        if existing_merchant:
            raise Conflict(f"Merchant with GST number {model.GSTNumber} already exists!")

    model_dict = model.dict()
    db_model = Merchant(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    merchant = db_model

    return merchant.__dict__

@trace_span("service: get_merchant_by_id")
def get_merchant_by_id(session: Session, merchant_id: str) -> MerchantResponseModel:
    merchant = session.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise NotFound(f"Merchant with id {merchant_id} not found")

    print_colorized_json(merchant)
    return merchant.__dict__

@trace_span("service: update_merchant")
def update_merchant(session: Session, merchant_id: str, model: MerchantUpdateModel) -> MerchantResponseModel:
    merchant = session.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise NotFound(f"Merchant with id {merchant_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Merchant).filter(Merchant.id == merchant_id).update(
        update_data, synchronize_session="auto")

    session.commit()
    session.refresh(merchant)
    return merchant.__dict__

@trace_span("service: delete_merchant")
def delete_merchant(session: Session, merchant_id: str) -> MerchantResponseModel:
    merchant = session.query(Merchant).get(merchant_id)
    if not merchant:
        raise NotFound(f"Merchant with id {merchant_id} not found")

    session.delete(merchant)

    session.commit()

    print_colorized_json(merchant)
    return merchant.__dict__

@trace_span("service: search_merchants")
def search_merchants(session: Session, filter) -> MerchantSearchResults:

    query = session.query(Merchant)
    if filter.Name:
        query = query.filter(Merchant.Name == filter.Name)
    if filter.Email:
        query = query.filter(Merchant.Email == filter.Email)
    if filter.Phone:
        query = query.filter(Merchant.Phone == filter.Phone)
    if filter.TaxNumber:
        query = query.filter(Merchant.TaxNumber == filter.TaxNumber)
    merchants = query.all()

    results = MerchantSearchResults(
        TotalCount=len(merchants),
        ItemsPerPage=filter.ItemsPerPage,
        PageNumber=filter.PageNumber,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=merchants
    )

    return results.__dict__

@trace_span("service: delete_merchant")
def delete_merchant(session: Session, merchant_id: str):
    merchant = session.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise NotFound(f"Merchant with id {merchant_id} not found")
    session.delete(merchant)
    session.commit()
    return True
