from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config.config import get_settings
from app.common.logger import logger
from .base import Base
from .database_initializer import initialize_database, test_database_connection, create_tables_if_not_exist

# Import all models to ensure they're registered
from .models import Address, Cart, Coupon, Customer, Merchant, Order
from .models import OrderCoupon, OrderLineItem, OrderType, OrderHistory, PaymentTransaction, customer_address

settings = get_settings()

# Initialize database and create tables
def setup_database():
    """Setup database with proper error handling"""
    try:
        # Initialize database (create if doesn't exist)
        if not initialize_database():
            logger.error("[SQLAlchemy] Failed to initialize database")
            return False
        
        # Test connection
        if not test_database_connection():
            logger.error("[SQLAlchemy] Failed to connect to database")
            return False
        
        # Create tables
        if not create_tables_if_not_exist():
            logger.error("[SQLAlchemy] Failed to create tables")
            return False
            
        logger.info("[SQLAlchemy] Database setup completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"[SQLAlchemy] Database setup failed: {e}")
        return False

# Setup database on module import
setup_database()

print(settings.DB_CONNECTION_STRING)
engine = create_engine(settings.DB_CONNECTION_STRING, echo=False)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session()-> Session:
    return LocalSession()
