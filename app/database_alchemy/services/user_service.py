import datetime as dt
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database_alchemy.models.user import User
from app.database_alchemy.models.user_role import UserRole
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.user import UserCreateModel, UserSearchFilters, UserUpdateModel, UserResponseModel, UserSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from app.telemetry.tracing import trace_span

@trace_span("service: create_user")
def create_user(session: Session, model: UserCreateModel) -> UserResponseModel:
 
    if model.Email != None and model.Email != "":
        existing_user = session.query(User).filter(func.lower(User.Email) == func.lower(model.Email)).first()
        if existing_user:
            raise Conflict(f"User with email {model.Email} already exists!")

    if model.Phone != None and model.Phone != "":
        existing_user = session.query(User).filter(User.Phone == model.Phone).first()
        if existing_user:
            raise Conflict(f"User with phone {model.Phone} already exists!")
          
    model.Password = hash_password(model.Password)
    model_dict = model.dict()
    model_dict.pop('RoleId', None)
    db_model = User(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    
    user_role = UserRole(UserId=db_model.id, RoleId=model.RoleId)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(user_role)
    session.commit()
    
    temp = session.refresh(db_model)
    user = db_model
    return user.__dict__

@trace_span("service: get_user_by_id")
def get_user_by_id(session: Session, user_id: str) -> UserResponseModel:
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFound(f"User with id {user_id} not found")
    return user.__dict__

@trace_span("service: update_user")
def update_user(session: Session, user_id: str, model: UserUpdateModel) -> UserResponseModel:
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFound(f"User with id {user_id} not found")
    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(User).filter(User.id == user_id).update(
        update_data, synchronize_session="auto")
    session.commit()
    session.refresh(user)
    return user.__dict__

@trace_span("service: search_users")
def search_users(session: Session, filter: UserSearchFilters) -> UserSearchResults:

    query = session.query(User)
    
    if filter.RoleId:
        query = query.filter(User.RoleId)   
    if filter.UserName:
        query = query.filter(User.UserName.like(f'%{filter.UserName}%'))
    if filter.Email:
        query = query.filter(User.Email.like(f'%{filter.Email}%'))
    if filter.Phone:
        query = query.filter(User.Phone.like(f'%{filter.Phone}%'))
    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(User, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(User, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    users = query.all()

    items = list(map(lambda x: x.__dict__, users))

    results = UserSearchResults(
        TotalCount=len(users),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results

@trace_span("service: delete_user")
def delete_user(session: Session, user_id: str):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFound(f"Api client with id {user_id} not found")
    session.delete(user)
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