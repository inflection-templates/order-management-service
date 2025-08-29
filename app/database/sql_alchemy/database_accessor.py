from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config.config import get_settings
from typing import Optional

# Load config
settings = get_settings()

# Create the engine only if we're using MySQL
def _create_engine():
    if settings.DB_DIALECT.lower() == "mysql":
        return create_engine(settings.DB_CONNECTION_STRING, echo=False)
    else:
        raise RuntimeError("SQLAlchemy engine requested but DB_DIALECT is not 'mysql'")

# Create engine and session factory
try:
    engine = _create_engine()
    LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    # If engine creation fails, set to None
    engine = None
    LocalSession = None

# Session function
def get_db_session() -> Session:
    if LocalSession is None:
        raise RuntimeError("SQLAlchemy not configured. Check DB_DIALECT setting.")
    return LocalSession()
