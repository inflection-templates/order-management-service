from app.database.orm_factory import orm_factory
from app.config.config import get_settings

def print_orm_status():
    """Print current ORM status and configuration"""
    settings = get_settings()
    
    print("=" * 50)
    print("🔧 ORM CONFIGURATION STATUS")
    print("=" * 50)
    print(f"Current ORM: {orm_factory.orm_type.value.upper()}")
    print(f"Raw Config Value: '{settings.ORM_TYPE}'")
    print(f"Available ORMs: {[orm.value for orm in orm_factory.ORMType]}")
    print(f"Database: {settings.DB_NAME}")
    print("=" * 50)

def get_orm_info():
    """Get ORM information as a dictionary"""
    settings = get_settings()
    return {
        "current_orm": orm_factory.orm_type.value,
        "raw_config": settings.ORM_TYPE,
        "available_orms": [orm.value for orm in orm_factory.ORMType],
        "database": settings.DB_NAME,
        "connection_info": {
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "database": settings.DB_NAME
        }
    }

if __name__ == "__main__":
    print_orm_status()
