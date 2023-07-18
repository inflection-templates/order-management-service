from fastapi import APIRouter
from app.config.constants import API_PREFIX
from .order.order_routes import router as order_router
from .customer.customer_routes import router as customer_router
from .address.address_routes import router as address_router
from .merchant.merchant_routes import router as merchant_router
from .cart.cart_routes import router as cart_router
from .coupon.coupon_routes import router as coupon_router
from .payment_transaction.payment_transaction_routes import router as payment_transaction_router


router = APIRouter(prefix=API_PREFIX)

def add_routes():
    router.include_router(order_router)
    router.include_router(customer_router)
    router.include_router(address_router)
    router.include_router(merchant_router)
    router.include_router(cart_router)
    router.include_router(coupon_router)
    router.include_router(payment_transaction_router)

    # Add other routes here

add_routes()
