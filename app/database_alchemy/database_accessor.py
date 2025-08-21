from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config.config import get_settings

# Load config
settings = get_settings()

# Create the engine
engine = create_engine(settings.DB_CONNECTION_STRING, echo=False)

# Session factory
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Session function
def get_db_session() -> Session:
    return LocalSession()
