import datetime as dt
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.user import User
from app.database.models.user_role import UserRole
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

@trace_span("service: seed_system_admin")
def seed_system_admin(session: Session) -> bool:
    """Seed system admin user from seed data file"""
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
    from app.database.models.tenant import Tenant
    from sqlalchemy import func
    
    try:
        print("Seeding default user...")
        logger.info("Seeding system admin user...")
        seed_data = load_json_seed_file("system.admin.seed.json")
        
        # Check if user with email already exists
        existing_user = session.query(User).filter(func.lower(User.Email) == func.lower(seed_data.get("Email", ""))).first()
        if existing_user:
            logger.info(f"User with email '{seed_data.get('Email')}' already exists. Skipping seed.")
            return True
        
        # Get default tenant
        default_tenant = session.query(Tenant).filter(func.lower(Tenant.Code) == "default").first()
        if not default_tenant:
            logger.error("Default tenant not found. Please seed tenant first.")
            return False
        
        # Get default role (System Admin) - we'll create it if it doesn't exist
        from app.database.models.role import Role
        admin_role = session.query(Role).filter(Role.RoleName == "System Admin").first()
        if not admin_role:
            # Create a temporary role ID, will be fixed after role seeding
            admin_role_id = 1
        else:
            admin_role_id = admin_role.id
        
        # Create user from seed data
        user_model = UserCreateModel(
            FirstName=seed_data.get("FirstName", "system-admin"),
            Email=seed_data.get("Email", "sys.admin@example.com"),
            UserName=seed_data.get("UserName", "admin"),
            Password=seed_data.get("Password", "ChangeMe123!"),
            Phone=seed_data.get("PhoneNumber", "0000000000"),
            CountryCode=seed_data.get("PhoneCode", "+91"),
            RoleId=admin_role_id
        )
        
        # Set TenantId directly on the model dict since it's not in the schema
        model_dict = user_model.dict()
        model_dict.pop('RoleId', None)
        # Hash the password before storing (same as client_app)
        model_dict['Password'] = hash_password(model_dict['Password'])
        db_model = User(**model_dict)
        db_model.TenantId = default_tenant.id
        db_model.UpdatedAt = dt.datetime.now()
        session.add(db_model)
        session.commit()
        
        # Create user role relationship if role exists
        if admin_role:
            user_role = UserRole(UserId=db_model.id, RoleId=admin_role_id)
            session.add(user_role)
            session.commit()
        
        logger.info(f"System admin user '{seed_data.get('UserName', 'admin')}' seeded successfully.")
        return True
    except Exception as e:
        logger.error(f"Error seeding system admin: {str(e)}")
        return False