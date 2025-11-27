import datetime as dt
import json
from app.common.utils import print_colorized_json
from app.database.models.organization import Organization
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.organization import OrganizationCreateModel, OrganizationUpdateModel, OrganizationResponseModel, OrganizationSearchFilter, OrganizationSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from app.telemetry.tracing import trace_span

###############################################################################

@trace_span("service: create_organization")
def create_organization(session: Session, model: OrganizationCreateModel) -> OrganizationResponseModel:
    # Check if organization with same code exists
    existing_org = session.query(Organization).filter(func.lower(Organization.Code) == func.lower(model.Code)).first()
    if existing_org:
        raise Conflict(f"Organization with code {model.Code} already exists!")
    
    model_dict = model.dict()
    db_model = Organization(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    
    print_colorized_json(db_model)
    return db_model.__dict__

@trace_span("service: get_organization_by_id")
def get_organization_by_id(session: Session, organization_id: str) -> OrganizationResponseModel:
    organization = session.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        raise NotFound(f"Organization with id {organization_id} not found")
    
    print_colorized_json(organization)
    return organization.__dict__

@trace_span("service: get_organization_by_code")
def get_organization_by_code(session: Session, code: str) -> OrganizationResponseModel:
    organization = session.query(Organization).filter(func.lower(Organization.Code) == func.lower(code)).first()
    if not organization:
        raise NotFound(f"Organization with code {code} not found")
    return organization.__dict__

@trace_span("service: update_organization")
def update_organization(session: Session, organization_id: str, model: OrganizationUpdateModel) -> OrganizationResponseModel:
    organization = session.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        raise NotFound(f"Organization with id {organization_id} not found")
    
    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Organization).filter(Organization.id == organization_id).update(
        update_data, synchronize_session="auto")
    
    session.commit()
    session.refresh(organization)
    
    print_colorized_json(organization)
    return organization.__dict__

@trace_span("service: search_organizations")
def search_organizations(session: Session, filter: OrganizationSearchFilter) -> OrganizationSearchResults:
    query = session.query(Organization)
    
    if filter.Name:
        query = query.filter(Organization.Name.like(f'%{filter.Name}%'))
    if filter.Code:
        query = query.filter(Organization.Code == filter.Code)
    if filter.TenantId:
        query = query.filter(Organization.TenantId == filter.TenantId)
    if filter.IsActive is not None:
        query = query.filter(Organization.IsActive == filter.IsActive)
    
    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(Organization, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(Organization, filter.OrderBy)
    
    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))
    
    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)
    
    organizations = query.all()
    
    items = list(map(lambda x: x.__dict__, organizations))
    
    results = OrganizationSearchResults(
        TotalCount=len(organizations),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )
    
    return results

@trace_span("service: delete_organization")
def delete_organization(session: Session, organization_id: str):
    organization = session.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        raise NotFound(f"Organization with id {organization_id} not found")
    session.delete(organization)
    session.commit()
    return True

@trace_span("service: seed_default_organization")
def seed_default_organization(session: Session) -> bool:
    """Seed default organization from seed data file"""
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
        print("Seeding default organization...")
        logger.info("Seeding default organization...")
        seed_data = load_json_seed_file("default.organization.seed.json")
        
        # Check if organization with code already exists
        existing_org = session.query(Organization).filter(func.lower(Organization.Code) == func.lower(seed_data.get("Code", ""))).first()
        if existing_org:
            logger.info(f"Organization with code '{seed_data.get('Code')}' already exists. Skipping seed.")
            return True
        
        # Get default tenant
        from app.database.models.tenant import Tenant
        tenant_id = None
        tenant_id_value = seed_data.get("TenantId", "")
        if tenant_id_value and tenant_id_value.strip():
            # If TenantId is provided in seed data, use it
            tenant_id = tenant_id_value
        else:
            # Otherwise, try to get default tenant
            default_tenant = session.query(Tenant).filter(func.lower(Tenant.Code) == "default").first()
            tenant_id = default_tenant.id if default_tenant else None
        
        # Create organization directly (bypass service function to avoid verbose output)
        db_model = Organization(
            Name=seed_data.get("Name", "Default Organization"),
            Code=seed_data.get("Code", "default"),
            Description=seed_data.get("Description"),
            Domain=seed_data.get("Domain"),
            Industry=seed_data.get("Industry"),
            WebsiteUrl=seed_data.get("WebsiteUrl"),
            LogoUrl=seed_data.get("LogoUrl"),
            ContactEmail=seed_data.get("ContactEmail"),
            ContactPhone=seed_data.get("ContactPhone"),
            Address=seed_data.get("Address"),
            City=seed_data.get("City"),
            State=seed_data.get("State"),
            PostalCode=seed_data.get("PostalCode"),
            Country=seed_data.get("Country"),
            TenantId=tenant_id,
            IsActive=True
        )
        db_model.UpdatedAt = dt.datetime.now()
        session.add(db_model)
        session.commit()
        logger.info(f"Default organization '{seed_data.get('Name', 'Default Organization')}' seeded successfully.")
        return True
    except Exception as e:
        logger.error(f"Error seeding default organization: {str(e)}")
        return False

