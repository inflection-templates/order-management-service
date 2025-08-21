import datetime as dt
import secrets
from app.common.utils import print_colorized_json
from app.database_sqlmodel.models.api_client import ApiClient
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.api_client import ApiClientCreateModel, ApiClientUpdateModel, ApiClientResponseModel, ApiClientsSearchFilter, ApiClientSearchResults
from sqlmodel import Session, select, asc, desc, func
from app.telemetry.tracing import trace_span
from passlib.context import CryptContext

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@trace_span("service: create_api_client")
def create_api_client(session: Session, model: ApiClientCreateModel) -> ApiClientResponseModel:
    client = None
 
    if model.Email != None and model.Email != "":
        existing_client = session.exec(select(ApiClient).filter(func.lower(ApiClient.Email) == func.lower(model.Email))).first()
        if existing_client:
            raise Conflict(f"Client with email {model.Email} already exists!")

    if model.Phone != None and model.Phone != "":
        existing_client = session.exec(select(ApiClient).filter(ApiClient.Phone == model.Phone)).first()
        if existing_client:
            raise Conflict(f"Client with phone {model.Phone} already exists!")

    model.ApiKey = secrets.token_urlsafe(32)
    model.Password = hash_password(model.Password)
    model_dict = model.dict()
    db_model = ApiClient(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    client = db_model

    return client.dict()

@trace_span("service: get_api_client_by_id")
def get_api_client_by_id(session: Session, api_client_id: str) -> ApiClientResponseModel:
    client = session.exec(select(ApiClient).filter(ApiClient.id == api_client_id)).first()
    if not client:
        raise NotFound(f"API Client with id {api_client_id} not found!")
    return client.dict()

@trace_span("service: update_api_client")
def update_api_client(session: Session, api_client_id: str, model: ApiClientUpdateModel) -> ApiClientResponseModel:
    client = session.exec(select(ApiClient).filter(ApiClient.id == api_client_id)).first()
    if not client:
        raise NotFound(f"API Client with id {api_client_id} not found!")
    
    model_dict = model.dict(exclude_unset=True)
    if 'Password' in model_dict and model_dict['Password']:
        model_dict['Password'] = hash_password(model_dict['Password'])
    
    for key, value in model_dict.items():
        setattr(client, key, value)
    
    client.UpdatedAt = dt.datetime.now()
    session.add(client)
    session.commit()
    session.refresh(client)
    
    return client.dict()

@trace_span("service: search_api_clients")
def search_api_clients(session: Session, filter: ApiClientsSearchFilter) -> ApiClientSearchResults:
    query = select(ApiClient)
    
    if filter.Email:
        query = query.filter(func.lower(ApiClient.Email).contains(func.lower(filter.Email)))
    if filter.Phone:
        query = query.filter(ApiClient.Phone.contains(filter.Phone))
    if filter.ClientName:
        query = query.filter(func.lower(ApiClient.ClientName).contains(func.lower(filter.ClientName)))
    if filter.FirstName:
        query = query.filter(func.lower(ApiClient.FirstName).contains(func.lower(filter.FirstName)))
    if filter.LastName:
        query = query.filter(func.lower(ApiClient.LastName).contains(func.lower(filter.LastName)))
    
    # Handle sorting
    if filter.SortField and filter.SortOrder:
        sort_field = getattr(ApiClient, filter.SortField, None)
        if sort_field:
            if filter.SortOrder.lower() == 'desc':
                query = query.order_by(desc(sort_field))
            else:
                query = query.order_by(asc(sort_field))
    
    # Handle pagination
    total_count = len(session.exec(query).all())
    
    if filter.PageSize and filter.PageNumber:
        offset = (filter.PageNumber - 1) * filter.PageSize
        query = query.offset(offset).limit(filter.PageSize)
    
    clients = session.exec(query).all()
    
    return ApiClientSearchResults(
        Items=[client.dict() for client in clients],
        TotalCount=total_count,
        PageNumber=filter.PageNumber or 1,
        PageSize=filter.PageSize or total_count
    )

@trace_span("service: delete_api_client")
def delete_api_client(session: Session, api_client_id: str):
    client = session.exec(select(ApiClient).filter(ApiClient.id == api_client_id)).first()
    if not client:
        raise NotFound(f"API Client with id {api_client_id} not found!")
    
    session.delete(client)
    session.commit()
    
    return True

# Function to hash the password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return

