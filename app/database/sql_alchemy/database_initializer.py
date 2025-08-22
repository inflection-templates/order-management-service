import logging
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from app.config.config import get_settings

logger = logging.getLogger(__name__)

# Global flag to prevent multiple initializations
_database_initialized = False

def initialize_database() -> bool:
    """
    Initialize the database by creating it if it doesn't exist.
    Returns True if successful, False otherwise.
    """
    global _database_initialized
    
    if _database_initialized:
        logger.debug("[SQLAlchemy] Database already initialized, skipping...")
        return True
    
    settings = get_settings()
    
    try:
        # Create connection to MySQL server without specifying database
        server_connection_string = f"{settings.DB_DIALECT}+{settings.DB_DRIVER}://{settings.DB_USER_NAME}:{settings.DB_USER_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"
        
        # logger.info(f"[SQLAlchemy] Connecting to MySQL server at {settings.DB_HOST}:{settings.DB_PORT}")
        
        # Create engine for server connection
        server_engine = create_engine(server_connection_string, echo=False)
        
        # Test server connection
        with server_engine.connect() as connection:
            # logger.info("[SQLAlchemy] Successfully connected to MySQL server")
            
            # Check if database exists
            result = connection.execute(
                text(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{settings.DB_NAME}'")
            )
            
            if result.fetchone() is None:
                # Database doesn't exist, create it
                logger.info(f"[SQLAlchemy] Database '{settings.DB_NAME}' not found. Creating...")
                connection.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))
                connection.commit()
                logger.info(f"[SQLAlchemy] Database '{settings.DB_NAME}' created successfully!")
            else:
                logger.info(f"[SQLAlchemy] Database '{settings.DB_NAME}' already exists")
            
            logger.info(f"[SQLAlchemy] Connecting to '{settings.DB_NAME}'")
            
        server_engine.dispose()
        _database_initialized = True
        return True
        
    except OperationalError as e:
        logger.error(f"[SQLAlchemy] Failed to connect to server: {e}")
        return False
    except ProgrammingError as e:
        logger.error(f"[SQLAlchemy] Failed to create database: {e}")
        return False
    except Exception as e:
        logger.error(f"[SQLAlchemy] Unexpected error during database initialization: {e}")
        return False

def test_database_connection() -> bool:
    """
    Test connection to the specific database.
    Returns True if successful, False otherwise.
    """
    settings = get_settings()
    
    try:
        # Test connection to the specific database
        engine = create_engine(settings.DB_CONNECTION_STRING, echo=False)
        
        with engine.connect() as connection:
            # Simple test query
            result = connection.execute(text("SELECT 1"))
            if result.fetchone():
                logger.debug(f"[SQLAlchemy] Successfully connected to database '{settings.DB_NAME}'")
                engine.dispose()
                return True
                
    except OperationalError as e:
        logger.error(f"[SQLAlchemy] Failed to connect to database '{settings.DB_NAME}': {e}")
        return False
    except Exception as e:
        logger.error(f"[SQLAlchemy] Unexpected error during database connection test: {e}")
        return False
    
    return False

# Global flag for table creation
_tables_created = False

def create_tables_if_not_exist():
    """
    Create all tables if they don't exist.
    This function imports all models and creates the tables.
    """
    global _tables_created
    
    if _tables_created:        
        return True
    
    try:
        from sqlalchemy import create_engine
        from app.config.config import get_settings
        from app.database.sql_alchemy.base import Base
        
        # Import all models to ensure they're registered with Base
        from app.database.sql_alchemy.models import (
            Address, Cart, Coupon, Customer, Merchant, Order,
            OrderCoupon, OrderLineItem, OrderType, OrderHistory,
            PaymentTransaction, customer_address
        )
        
        settings = get_settings()
        engine = create_engine(settings.DB_CONNECTION_STRING, echo=False)
        
        # logger.info("[SQLAlchemy] Creating database tables...")
        Base.metadata.create_all(bind=engine)
        # logger.info("[SQLAlchemy] Database tables created successfully!")
        
        engine.dispose()
        _tables_created = True
        return True
        
    except Exception as e:
        logger.error(f"[SQLAlchemy] Failed to create tables: {e}")
        return False
