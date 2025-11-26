"""
Seeder module for initializing database with seed data.
Similar to Node.js service skeleton seeding functionality.
"""
import json
import os
from pathlib import Path
from app.common.logger import logger

def load_json_seed_file(filename: str):
    """
    Load JSON seed file from seed.data directory.
    Similar to Node.js Helper.loadJSONSeedFile
    """
    # Get the project root directory using current working directory (where main.py is run from)
    project_root = Path.cwd()
    seed_data_path = project_root / "seed.data" / filename
    
    if not seed_data_path.exists():
        raise FileNotFoundError(f"Seed file not found: {seed_data_path}")
    
    with open(seed_data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

class Seeder:
    """
    Main seeder class that orchestrates database seeding.
    Similar to Node.js Seeder class.
    """
    
    def __init__(self):
        pass
    
    def init(self):
        """
        Initialize seeding process.
        Order: Tenant -> User -> Role -> Client App
        """
        from app.database.database_accessor import get_db_session
        from app.database.services import tenant_service
        from app.database.services import user_service
        from app.database.services import role_service
        from app.database.services import api_client_service
        
        session = get_db_session()
        try:
            logger.info("Starting database seeding...")
            
            # 1. Seed default tenant
            tenant_service.seed_default_tenant(session)
            
            # 2. Seed system admin user
            user_service.seed_system_admin(session)
            
            # 3. Seed default roles
            role_service.seed_default_roles(session)
            
            # 4. Seed default client apps
            api_client_service.seed_default_clients(session)
            
            logger.info("Database seeding completed successfully.")
        except Exception as e:
            logger.error(f"Error during seeding: {str(e)}")
            raise
        finally:
            session.close()

