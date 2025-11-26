import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.api_client import ApiClient
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

@trace_span("service: seed_default_clients")
def seed_default_clients(session: Session) -> bool:
    """Seed default client apps from seed data file"""
    import json
    from pathlib import Path
    from app.common.logger import logger
    
    def load_json_seed_file(filename: str):
        """Load JSON seed file from seed.data directory"""
        # Get project root using current working directory (where main.py is run from)
        project_root = Path.cwd()
        seed_data_path = project_root / "seed.data" / filename
        
        if not seed_data_path.exists():
            raise FileNotFoundError(f"Seed file not found: {seed_data_path}")
        
        with open(seed_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    from app.database.models.user import User
    from sqlalchemy import func
    
    try:
        print("Seeding default client apps...")
        logger.info("Seeding default client apps...")
        clients_data = load_json_seed_file("internal.clients.seed.json")
        
        if not isinstance(clients_data, list):
            clients_data = [clients_data]
        
        # Get first user as owner (should be system admin)
        users = session.query(User).all()
        if len(users) == 0:
            logger.warning("No users found. Seed users before client apps.")
            return False
        
        owner = users[0]
        
        for client_data in clients_data:
            client_code = client_data.get("ClientCode", "")
            
            # Check if client with code already exists
            existing_client = session.query(ApiClient).filter(ApiClient.ClientCode == client_code).first()
            if existing_client:
                logger.info(f"Client with code '{client_code}' already exists. Skipping.")
                continue
            
            # Create client app directly (bypass service function to avoid verbose output)
            from app.database.services.api_client_service import hash_password
            import secrets
            
            db_model = ApiClient(
                ClientCode=client_code,
                ClientName=client_data.get("ClientName", ""),
                Email=client_data.get("Email", "support@example.com"),
                Password=hash_password(client_data.get("Password", "ChangeMe123!")),
                ApiKey=client_data.get("ApiKey", "api") or secrets.token_urlsafe(32),
                IsPrivileged=client_data.get("IsPrivileged", False),
                CountryCode="+91",
                Phone="0000000000",
                ClientInterfaceType="MobileApp"
            )
            db_model.UpdatedAt = dt.datetime.now()
            session.add(db_model)
            session.commit()
            logger.info(f"Client app '{client_code}' created successfully.")
        
        logger.info("Default client apps seeded successfully.")
        return True
    except Exception as e:
        logger.error(f"Error seeding default client apps: {str(e)}")
        return False

from passlib.context import CryptContext

# Initialize passlib context for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash the password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)