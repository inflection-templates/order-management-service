import datetime as dt
import json
from app.common.utils import print_colorized_json
from app.database.models.tenant import Tenant
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.tenant import TenantCreateModel, TenantUpdateModel, TenantResponseModel, TenantSearchFilter, TenantSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from app.telemetry.tracing import trace_span

###############################################################################

@trace_span("service: create_tenant")
def create_tenant(session: Session, model: TenantCreateModel) -> TenantResponseModel:
    # Check if tenant with same code exists
    existing_tenant = session.query(Tenant).filter(func.lower(Tenant.Code) == func.lower(model.Code)).first()
    if existing_tenant:
        raise Conflict(f"Tenant with code {model.Code} already exists!")
    
    model_dict = model.dict()
    db_model = Tenant(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    
    print_colorized_json(db_model)
    return db_model.__dict__

@trace_span("service: get_tenant_by_id")
def get_tenant_by_id(session: Session, tenant_id: str) -> TenantResponseModel:
    tenant = session.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise NotFound(f"Tenant with id {tenant_id} not found")
    
    print_colorized_json(tenant)
    return tenant.__dict__

@trace_span("service: get_tenant_by_code")
def get_tenant_by_code(session: Session, code: str) -> TenantResponseModel:
    tenant = session.query(Tenant).filter(func.lower(Tenant.Code) == func.lower(code)).first()
    if not tenant:
        raise NotFound(f"Tenant with code {code} not found")
    return tenant.__dict__

@trace_span("service: update_tenant")
def update_tenant(session: Session, tenant_id: str, model: TenantUpdateModel) -> TenantResponseModel:
    tenant = session.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise NotFound(f"Tenant with id {tenant_id} not found")
    
    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Tenant).filter(Tenant.id == tenant_id).update(
        update_data, synchronize_session="auto")
    
    session.commit()
    session.refresh(tenant)
    
    print_colorized_json(tenant)
    return tenant.__dict__

@trace_span("service: search_tenants")
def search_tenants(session: Session, filter: TenantSearchFilter) -> TenantSearchResults:
    query = session.query(Tenant)
    
    if filter.Name:
        query = query.filter(Tenant.Name.like(f'%{filter.Name}%'))
    if filter.Code:
        query = query.filter(Tenant.Code == filter.Code)
    if filter.IsActive is not None:
        query = query.filter(Tenant.IsActive == filter.IsActive)
    
    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(Tenant, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(Tenant, filter.OrderBy)
    
    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))
    
    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)
    
    tenants = query.all()
    
    items = list(map(lambda x: x.__dict__, tenants))
    
    results = TenantSearchResults(
        TotalCount=len(tenants),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )
    
    return results

@trace_span("service: delete_tenant")
def delete_tenant(session: Session, tenant_id: str):
    tenant = session.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise NotFound(f"Tenant with id {tenant_id} not found")
    session.delete(tenant)
    session.commit()
    return True

@trace_span("service: seed_default_tenant")
def seed_default_tenant(session: Session) -> bool:
    """Seed default tenant from seed data file"""
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
    
    try:
        print("Seeding default tenant...")
        logger.info("Seeding default tenant...")
        seed_data = load_json_seed_file("default.tenant.seed.json")
        
        # Check if tenant with code already exists
        existing_tenant = session.query(Tenant).filter(func.lower(Tenant.Code) == func.lower(seed_data.get("Code", ""))).first()
        if existing_tenant:
            logger.info(f"Tenant with code '{seed_data.get('Code')}' already exists. Skipping seed.")
            return True
        
        # Create tenant directly (bypass service function to avoid verbose output)
        db_model = Tenant(
            Name=seed_data.get("Name", "Default"),
            Code=seed_data.get("Code", "default"),
            Description=seed_data.get("Description"),
            IsActive=True,
            IsDefault=True
        )
        db_model.UpdatedAt = dt.datetime.now()
        session.add(db_model)
        session.commit()
        logger.info(f"Default tenant '{seed_data.get('Name', 'Default')}' seeded successfully.")
        return True
    except Exception as e:
        logger.error(f"Error seeding default tenant: {str(e)}")
        return False

