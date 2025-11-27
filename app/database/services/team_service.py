import datetime as dt
import json
from app.common.utils import print_colorized_json
from app.database.models.team import Team
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.team import TeamCreateModel, TeamUpdateModel, TeamResponseModel, TeamSearchFilter, TeamSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from app.telemetry.tracing import trace_span

###############################################################################

@trace_span("service: create_team")
def create_team(session: Session, model: TeamCreateModel) -> TeamResponseModel:
    # Check if team with same code exists
    existing_team = session.query(Team).filter(func.lower(Team.Code) == func.lower(model.Code)).first()
    if existing_team:
        raise Conflict(f"Team with code {model.Code} already exists!")
    
    model_dict = model.dict()
    # Convert Permissions list to JSON string
    if "Permissions" in model_dict and model_dict["Permissions"] is not None:
        model_dict["Permissions"] = json.dumps(model_dict["Permissions"])
    else:
        model_dict["Permissions"] = None
    
    db_model = Team(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    
    # Convert Permissions back to list for response
    if db_model.Permissions:
        db_model.Permissions = json.loads(db_model.Permissions)
    else:
        db_model.Permissions = []
    
    print_colorized_json(db_model)
    return db_model.__dict__

@trace_span("service: get_team_by_id")
def get_team_by_id(session: Session, team_id: str) -> TeamResponseModel:
    team = session.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise NotFound(f"Team with id {team_id} not found")
    
    # Convert Permissions JSON string to list
    if team.Permissions:
        team.Permissions = json.loads(team.Permissions)
    else:
        team.Permissions = []
    
    print_colorized_json(team)
    return team.__dict__

@trace_span("service: get_team_by_code")
def get_team_by_code(session: Session, code: str) -> TeamResponseModel:
    team = session.query(Team).filter(func.lower(Team.Code) == func.lower(code)).first()
    if not team:
        raise NotFound(f"Team with code {code} not found")
    
    # Convert Permissions JSON string to list
    if team.Permissions:
        team.Permissions = json.loads(team.Permissions)
    else:
        team.Permissions = []
    
    return team.__dict__

@trace_span("service: update_team")
def update_team(session: Session, team_id: str, model: TeamUpdateModel) -> TeamResponseModel:
    team = session.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise NotFound(f"Team with id {team_id} not found")
    
    update_data = model.dict(exclude_unset=True)
    # Convert Permissions list to JSON string
    if "Permissions" in update_data and update_data["Permissions"] is not None:
        update_data["Permissions"] = json.dumps(update_data["Permissions"])
    
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Team).filter(Team.id == team_id).update(
        update_data, synchronize_session="auto")
    
    session.commit()
    session.refresh(team)
    
    # Convert Permissions back to list for response
    if team.Permissions:
        team.Permissions = json.loads(team.Permissions)
    else:
        team.Permissions = []
    
    print_colorized_json(team)
    return team.__dict__

@trace_span("service: search_teams")
def search_teams(session: Session, filter: TeamSearchFilter) -> TeamSearchResults:
    query = session.query(Team)
    
    if filter.Name:
        query = query.filter(Team.Name.like(f'%{filter.Name}%'))
    if filter.Code:
        query = query.filter(Team.Code == filter.Code)
    if filter.OrganizationId:
        query = query.filter(Team.OrganizationId == filter.OrganizationId)
    if filter.OwnerUserId:
        query = query.filter(Team.OwnerUserId == filter.OwnerUserId)
    if filter.IsActive is not None:
        query = query.filter(Team.IsActive == filter.IsActive)
    
    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(Team, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(Team, filter.OrderBy)
    
    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))
    
    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)
    
    teams = query.all()
    
    # Convert Permissions JSON string to list for each team
    items = []
    for team in teams:
        team_dict = team.__dict__.copy()
        if team.Permissions:
            team_dict["Permissions"] = json.loads(team.Permissions)
        else:
            team_dict["Permissions"] = []
        items.append(team_dict)
    
    results = TeamSearchResults(
        TotalCount=len(teams),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )
    
    return results

@trace_span("service: delete_team")
def delete_team(session: Session, team_id: str):
    team = session.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise NotFound(f"Team with id {team_id} not found")
    session.delete(team)
    session.commit()
    return True

@trace_span("service: seed_default_team")
def seed_default_team(session: Session) -> bool:
    """Seed default team from seed data file"""
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
        print("Seeding default team...")
        logger.info("Seeding default team...")
        seed_data = load_json_seed_file("default.team.seed.json")
        
        # Check if team with code already exists
        existing_team = session.query(Team).filter(func.lower(Team.Code) == func.lower(seed_data.get("Code", ""))).first()
        if existing_team:
            logger.info(f"Team with code '{seed_data.get('Code')}' already exists. Skipping seed.")
            return True
        
        # Get default organization
        from app.database.models.organization import Organization
        organization_id = None
        organization_id_value = seed_data.get("OrganizationId", "")
        if organization_id_value and organization_id_value.strip():
            organization_id = organization_id_value
        else:
            default_org = session.query(Organization).filter(func.lower(Organization.Code) == "default").first()
            organization_id = default_org.id if default_org else None
        
        # Get system admin user as owner
        from app.database.models.user import User
        owner_user_id = None
        owner_user_id_value = seed_data.get("OwnerUserId", "")
        if owner_user_id_value and owner_user_id_value.strip():
            owner_user_id = owner_user_id_value
        else:
            # Get first user (should be system admin)
            system_admin = session.query(User).filter(func.lower(User.UserName) == "admin").first()
            owner_user_id = system_admin.id if system_admin else None
        
        # Handle Permissions
        permissions = seed_data.get("Permissions", [])
        permissions_json = json.dumps(permissions) if permissions else None
        
        # Create team directly (bypass service function to avoid verbose output)
        db_model = Team(
            Name=seed_data.get("Name", "Default Team"),
            Code=seed_data.get("Code", "default"),
            Description=seed_data.get("Description"),
            OrganizationId=organization_id,
            OwnerUserId=owner_user_id,
            Permissions=permissions_json,
            IsActive=True
        )
        db_model.UpdatedAt = dt.datetime.now()
        session.add(db_model)
        session.commit()
        logger.info(f"Default team '{seed_data.get('Name', 'Default Team')}' seeded successfully.")
        return True
    except Exception as e:
        logger.error(f"Error seeding default team: {str(e)}")
        return False

