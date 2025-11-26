import datetime as dt
import json
from fastapi import Query, Body
from app.common.utils import print_colorized_json
from app.database.database_accessor import LocalSession
from app.database.models.role import Role
from app.domain_types.schemas.role.role import RoleCreateModel, RoleResponseModel, RoleSearchFilter, RoleSearchResults, RoleUpdateModel
from sqlalchemy.orm import Session
from app.domain_types.miscellaneous.exceptions import NotFound
from sqlalchemy import asc, desc, func
from app.telemetry.tracing import trace_span

###############################################################################

@trace_span("service: create_role")
def create_role(session: Session, model: RoleCreateModel) -> RoleResponseModel:
    model_dict = model.dict()
    db_model = Role(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    role = db_model

    print_colorized_json(role)
    return role.__dict__

@trace_span("service: get_role_by_id")
def get_role_by_id(session: Session, role_id: str) -> RoleResponseModel:
    role = session.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise NotFound(f"Role with id {role_id} not found")

    print_colorized_json(role)
    return role.__dict__

@trace_span("service: update_role")
def update_role(session: Session, role_id: int, model: RoleUpdateModel) -> RoleResponseModel:
    role = session.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise NotFound(f"Role with id {role_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Role).filter(Role.id == role_id).update(
        update_data, synchronize_session="auto")

    session.commit()
    session.refresh(role)

    print_colorized_json(role)
    return role.__dict__

@trace_span("service: search_roles")
def search_roles(session: Session, filter: RoleSearchFilter) -> RoleSearchResults:

    query = session.query(Role)

    if filter.RoleName:
        query = query.filter(Role.RoleName.like(f'%{filter.RoleName}%'))
    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(Role, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(Role, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    roles = query.all()

    items = list(map(lambda x: x.__dict__, roles))

    results = RoleSearchResults(
        TotalCount=len(roles),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results

@trace_span("service: delete_role")
def delete_role(session: Session, role_id: str) -> RoleResponseModel:
    role = session.query(Role).get(role_id)
    if not role:
        raise NotFound(f"Role with id {role_id} not found")

    session.delete(role)

    session.commit()

    print_colorized_json(role)
    return role.__dict__

@trace_span("service: seed_default_roles")
def seed_default_roles(session: Session) -> bool:
    """Seed default roles from seed data file"""
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
    from app.database.models.user_role import UserRole
    from sqlalchemy import func
    
    try:
        print("Seeding default roles...")
        logger.info("Seeding default roles...")
        roles_data = load_json_seed_file("default.roles.seed.json")
        
        if not isinstance(roles_data, list):
            roles_data = [roles_data]
        
        system_admin_user = None
        system_admin_role = None
        
        for role_data in roles_data:
            role_name = role_data.get("RoleName", "")
            
            # Check if role already exists
            existing_role = session.query(Role).filter(Role.RoleName == role_name).first()
            if existing_role:
                logger.info(f"Role '{role_name}' already exists. Skipping.")
                if role_name == "System Admin":
                    system_admin_role = existing_role
                continue
            
            # Create role directly (bypass service function to avoid verbose output)
            db_model = Role(
                RoleName=role_name,
                Description=role_data.get("Description", "")
            )
            db_model.UpdatedAt = dt.datetime.now()
            session.add(db_model)
            session.commit()
            session.refresh(db_model)
            
            if role_name == "System Admin":
                system_admin_role = db_model
            
            logger.info(f"Role '{role_name}' created successfully.")
        
        # Assign System Admin role to system admin user if not already assigned
        if system_admin_role:
            system_admin_user = session.query(User).filter(func.lower(User.UserName) == "admin").first()
            if system_admin_user:
                existing_user_role = session.query(UserRole).filter(
                    UserRole.UserId == system_admin_user.id,
                    UserRole.RoleId == system_admin_role.id
                ).first()
                
                if not existing_user_role:
                    user_role = UserRole(UserId=system_admin_user.id, RoleId=system_admin_role.id)
                    session.add(user_role)
                    session.commit()
                    logger.info("System Admin role assigned to admin user.")
        
        logger.info("Default roles seeded successfully.")
        return True
    except Exception as e:
        logger.error(f"Error seeding default roles: {str(e)}")
        return False