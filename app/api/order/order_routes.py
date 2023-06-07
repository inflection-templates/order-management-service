from fastapi import APIRouter

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", status_code=200)
async def get_orders():
    return "get_orders"


