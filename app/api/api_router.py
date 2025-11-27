from fastapi import APIRouter
from app.config.constants import API_PREFIX
from .auth.auth_routes import router as auth_router
from .order.order_routes import router as order_router
from .customer.customer_routes import router as customer_router
from .address.address_routes import router as address_router
from .merchant.merchant_routes import router as merchant_router
from .cart.cart_routes import router as cart_router
from .coupon.coupon_routes import router as coupon_router
from .payment_transaction.payment_transaction_routes import router as payment_transaction_router
from .api_client.api_client_routes import router as api_client_router
from .user.user_routes import router as user_router
from .role.role_routes import router as role_router
from .tenant.tenant_routes import router as tenant_router
from .organization.organization_routes import router as organization_router

router = APIRouter(prefix=API_PREFIX)

def add_routes():
    router.include_router(auth_router)
    router.include_router(tenant_router)
    router.include_router(organization_router)
    router.include_router(role_router)
    router.include_router(user_router)
    router.include_router(order_router)
    router.include_router(customer_router)
    router.include_router(address_router)
    router.include_router(merchant_router)
    router.include_router(cart_router)
    router.include_router(coupon_router)
    router.include_router(payment_transaction_router)
    router.include_router(api_client_router)
    # Add other routes here

add_routes()
