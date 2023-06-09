from fastapi import APIRouter
from app.common.utils import print_colorized_json

from app.domain_types.order import OrderCreateModel, OrderResponseModel

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code=200)
async def get_orders():
    return "get_orders"

@router.post("/", status_code=201, response_model=OrderResponseModel|None)
async def create_order(model: OrderCreateModel):
    print_colorized_json(model)
    return None

