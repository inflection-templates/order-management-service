from typing import Generator
from pymongo.database import Database
from app.database.mongodb.database_initializer import get_database

def get_db_session() -> Generator[Database, None, None]:
    """Get MongoDB database session (compatible with existing interface)"""
    try:
        db = get_database()
        yield db
    except Exception as e:
        raise e
