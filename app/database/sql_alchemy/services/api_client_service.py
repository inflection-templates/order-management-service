import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.sql_alchemy.models.api_client import ApiClient
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.api_client import ApiClientCreateModel, ApiClientUpdateModel, ApiClientResponseModel, ApiClientsSearchFilter, ApiClientSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from app.telemetry.tracing import trace_span
import secrets

@trace_span("service: create_api_client")
def create_api_client(session: Session, model: ApiClientCreateModel) -> ApiClientResponseModel:
    client = None
 
    if model.Email != None and model.Email != "":
        existing_client = session.query(ApiClient).filter(func.lower(ApiClient.Email) == func.lower(model.Email)).first()
        if existing_client:
            raise Conflict(f"Client with email {model.Email} already exists!")

    if model.Phone != None and model.Phone != "":
        existing_client = session.query(ApiClient).filter(ApiClient.Phone == model.Phone).first()
        if existing_client:
            raise Conflict(f"Client with phone {model.Phone} already exists!")

    model.ApiKey = secrets.token_urlsafe(32)
    model.Password = hash_password(model.Password)
    model_dict = model.dict()
    db_model = ApiClient(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    client = db_model
    return client.__dict__

@trace_span("service: get_api_client_by_id")
def get_api_client_by_id(session: Session, api_client_id: str) -> ApiClientResponseModel:
    api_client = session.query(ApiClient).filter(ApiClient.id == api_client_id).first()
    if not api_client:
        raise NotFound(f"Client with id {api_client_id} not found")
    return api_client.__dict__

@trace_span("service: update_api_client")
def update_api_client(session: Session, api_client_id: str, model: ApiClientUpdateModel) -> ApiClientResponseModel:
    api_client = session.query(ApiClient).filter(ApiClient.id == api_client_id).first()
    if not api_client:
        raise NotFound(f"Client with id {api_client_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(ApiClient).filter(ApiClient.id == api_client_id).update(
        update_data, synchronize_session="auto")

    session.commit()
    session.refresh(api_client)
    return api_client.__dict__

@trace_span("service: search_api_clients")
def search_api_clients(session: Session, filter: ApiClientsSearchFilter) -> ApiClientSearchResults:

    query = session.query(ApiClient)

    if filter.ClientName:
        query = query.filter(ApiClient.ClientName.like(f'%{filter.ClientName}%'))
    if filter.Email:
        query = query.filter(ApiClient.Email.like(f'%{filter.Email}%'))
    if filter.ClientCode:
        query = query.filter(ApiClient.ClientCode == filter.ClientCode)
    if filter.Phone:
        query = query.filter(ApiClient.Phone.like(f'%{filter.Phone}%'))

    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(ApiClient, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(ApiClient, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    api_clients = query.all()

    items = list(map(lambda x: x.__dict__, api_clients))

    results = ApiClientSearchResults(
        TotalCount=len(api_clients),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results

@trace_span("service: delete_api_client")
def delete_api_client(session: Session, api_client_id: str):
    api_client = session.query(ApiClient).filter(ApiClient.id == api_client_id).first()
    if not api_client:
        raise NotFound(f"Api client with id {api_client_id} not found")
    session.delete(api_client)
    session.commit()
    return True

from passlib.context import CryptContext

# Initialize passlib context for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash the password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)