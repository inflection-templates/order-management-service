import json
from sqlmodel import SQLModel, Field, Column, DateTime, Text, Date
from app.common.utils import generate_uuid4
from typing import Optional
from datetime import datetime, date
from sqlalchemy import func

from .address import Address
from .api_client import ApiClient
from .auth_token import AuthToken
from .cart import Cart
from .coupon import Coupon
from .customer import Customer
from .customer_address import CustomerAddress
from .merchant import Merchant
from .order import Order
from .order_coupon import OrderCoupon
from .order_history import OrderHistory
from .order_line_item import OrderLineItem
from .order_payment import OrderPayment
from .order_type import OrderType
from .payment_transaction import PaymentTransaction
from .role import Role
from .tenant import Tenant
from .user import User
from .user_role import UserRole
from .user_external_auth import UserExternalAuth
from .user_login_session import UserLoginSession

# Import the customer_address table for the many-to-many relationship
try:
    from .customer_address import customer_address
except ImportError:
    # Fallback if customer_address is defined differently
    customer_address = CustomerAddress

__all__ = [
    "Address", "ApiClient", "AuthToken", "Cart", "Coupon", "Customer", "CustomerAddress", 
    "Merchant", "Order", "OrderCoupon", "OrderHistory", "OrderLineItem", 
    "OrderPayment", "OrderType", "PaymentTransaction", "Role", "Tenant", 
    "User", "UserRole", "UserExternalAuth", "UserLoginSession", "customer_address"
]


