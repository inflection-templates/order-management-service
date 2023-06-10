from fastapi import APIRouter, Depends
from app.common.utils import print_colorized_json
from app.database.database_accessor import DatabaseSession, get_db_session
from app.database.services import order_service
from app.domain_types.schemas.order import OrderCreateModel, OrderResponseModel

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
async def create_order(model: OrderCreateModel, db_session: DatabaseSession = Depends(get_db_session)):
    return order_service.create_order(db_session, model)
