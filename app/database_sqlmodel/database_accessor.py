from sqlmodel import SQLModel, create_engine, Session
from app.config.config import get_settings

# Import your models that inherit from SQLModel
from .models import (
    Address, Cart, Coupon, Customer, Merchant, Order,
    OrderCoupon, OrderLineItem, OrderType, OrderHistory,
    PaymentTransaction, customer_address
)

# Load config
settings = get_settings()

# Create the engine
engine = create_engine(settings.DB_CONNECTION_STRING, echo=False)

# Note: Table creation is now handled by the database initializer

# Session function
def get_db_session() -> Session:
    return Session(engine)