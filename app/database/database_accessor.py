from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DB_CONNECTION_STRING
)

# or
# engine = create_engine(
#     settings.DB_DIALECT,
#     username=settings.DB_USER_NAME,
#     password=settings.DB_USER_PASSWORD,
#     host=settings.DB_HOST,
#     port=settings.DB_PORT,
#     database=settings.DB_NAME,
#     pool_size=settings.DB_POOL_SIZE,
#     pool_recycle=settings.DB_POOL_RECYCLE,
# )

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DatabaseSession:
    ''' Dependency class for getting transactional session '''

    def __init__(self):
        self.db = self.get_db_session()
        pass

    def get_db_session(self):
        session = LocalSession()
        try:
            yield session
        finally:
            session.close()

def get_db_session()-> DatabaseSession:
    session = DatabaseSession()
    try:
        yield session
    finally:
        session.close()
