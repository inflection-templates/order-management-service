from fastapi import APIRouter, Depends, HTTPException, status
from app.config.constants import API_PREFIX, API_VERSION
from .order.order_routes import router as order_router

router = APIRouter(prefix=API_PREFIX)

def add_routes():
    router.include_router(order_router)
    # Add other routes here

add_routes()
