from .address import Address
from .customer import Customer
from .customer_address import CustomerAddress
from .order import Order
from .order_line_item import OrderLineItem
from .order_history import OrderHistory
from .order_type import OrderType
from .order_coupon import OrderCoupon
from .cart import Cart
from .coupon import Coupon
from .merchant import Merchant
from .payment_transaction import PaymentTransaction
from .api_client import ApiClient

# Authentication models - Import these before User to avoid circular dependencies
from .tenant import Tenant
from .auth_token import AuthToken
from .user_external_auth import UserExternalAuth

# User-related models - Import these before User
from .user.otp import Otp
from .user.user_login_session import UserLoginSession

# User and role models
# Import from packages - they will load from parent .py files via their __init__.py
# This avoids loading the same module twice which causes SQLAlchemy table registration errors
from .user import User
from .role import Role
from .user_role import UserRole
# from .role.role_permissions import RolePermission
# from .role.role_privileges import RolePrivilege
from .person.person import Person
from .person.person_role import PersonRole
from .person.person_addresses import PersonAddresses

