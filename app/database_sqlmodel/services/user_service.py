import datetime as dt
from app.common.utils import print_colorized_json
from app.database_sqlmodel.models.user import User
from app.database_sqlmodel.models.user_role import UserRole
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.user import UserCreateModel, UserSearchFilters, UserUpdateModel, UserResponseModel, UserSearchResults
from sqlmodel import Session, select, asc, desc, func
from app.telemetry.tracing import trace_span
from passlib.context import CryptContext

# Password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@trace_span("service: create_user")
def create_user(session: Session, model: UserCreateModel) -> UserResponseModel:
    if model.Email != None and model.Email != "":
        existing_user = session.exec(select(User).filter(func.lower(User.Email) == func.lower(model.Email))).first()
        if existing_user:
            raise Conflict(f"User with email {model.Email} already exists!")

    if model.Phone != None and model.Phone != "":
        existing_user = session.exec(select(User).filter(User.Phone == model.Phone)).first()
        if existing_user:
            raise Conflict(f"User with phone {model.Phone} already exists!")
          
    model.Password = hash_password(model.Password)
    model_dict = model.dict()
    model_dict.pop('RoleId', None)
    db_model = User(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    user = db_model

    # Handle role assignment if provided
    if hasattr(model, 'RoleId') and model.RoleId:
        user_role = UserRole(UserId=user.id, RoleId=model.RoleId)
        session.add(user_role)
        session.commit()

    return user.dict()

@trace_span("service: get_user_by_id")
def get_user_by_id(session: Session, user_id: str) -> UserResponseModel:
    user = session.exec(select(User).filter(User.id == user_id)).first()
    if not user:
        raise NotFound(f"User with id {user_id} not found!")
    return user.dict()

@trace_span("service: update_user")
def update_user(session: Session, user_id: str, model: UserUpdateModel) -> UserResponseModel:
    user = session.exec(select(User).filter(User.id == user_id)).first()
    if not user:
        raise NotFound(f"User with id {user_id} not found!")
    
    model_dict = model.dict(exclude_unset=True)
    if 'Password' in model_dict and model_dict['Password']:
        model_dict['Password'] = hash_password(model_dict['Password'])
    
    for key, value in model_dict.items():
        setattr(user, key, value)
    
    user.UpdatedAt = dt.datetime.now()
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user.dict()

@trace_span("service: search_users")
def search_users(session: Session, filter: UserSearchFilters) -> UserSearchResults:
    query = select(User)
    
    if filter.Email:
        query = query.filter(func.lower(User.Email).contains(func.lower(filter.Email)))
    if filter.Phone:
        query = query.filter(User.Phone.contains(filter.Phone))
    if filter.FirstName:
        query = query.filter(func.lower(User.FirstName).contains(func.lower(filter.FirstName)))
    if filter.LastName:
        query = query.filter(func.lower(User.LastName).contains(func.lower(filter.LastName)))
    
    # Handle sorting
    if filter.SortField and filter.SortOrder:
        sort_field = getattr(User, filter.SortField, None)
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
    
    users = session.exec(query).all()
    
    return UserSearchResults(
        Items=[user.dict() for user in users],
        TotalCount=total_count,
        PageNumber=filter.PageNumber or 1,
        PageSize=filter.PageSize or total_count
    )

@trace_span("service: delete_user")
def delete_user(session: Session, user_id: str):
    user = session.exec(select(User).filter(User.id == user_id)).first()
    if not user:
        raise NotFound(f"User with id {user_id} not found!")
    
    user.DeletedAt = dt.datetime.now()
    session.add(user)
    session.commit()
    
    return True

# Function to hash the password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
