from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config.config import get_settings
from .base import Base

from .models import Address, Cart, Coupon, Customer, Merchant, Order
from .models import OrderCoupon, OrderLineItem, OrderType, OrderHistory, PaymentTransaction

settings = get_settings()
print(settings.DB_CONNECTION_STRING)
engine = create_engine(settings.DB_CONNECTION_STRING, echo=False)
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
#     drivername=settings.DB_DRIVER,
#     echo=True,
# )

Base.metadata.create_all(bind=engine)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session()-> Session:
    return LocalSession()
