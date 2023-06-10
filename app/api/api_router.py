from fastapi import APIRouter
from app.config.constants import API_PREFIX
from .order import router as order_router
from .customer import router as customer_router

router = APIRouter(prefix=API_PREFIX)

def add_routes():
    router.include_router(order_router)
    router.include_router(customer_router)
    # Add other routes here

add_routes()
