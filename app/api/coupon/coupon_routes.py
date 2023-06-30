from fastapi import APIRouter, Depends, status
from app.api.coupon.coupon_handler import (
    create_coupon_,
    get_coupon_by_id_,
    update_coupon_,
    delete_coupon_,
    search_coupons_
)
from app.database.database_accessor import get_db_session
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.coupon import CouponCreateModel, CouponResponseModel, CouponUpdateModel, CouponSearchFilter, CouponSearchResults

###############################################################################

router = APIRouter(
    prefix="/coupons",
    tags=["coupons"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[CouponResponseModel|None])
async def create_coupon(model: CouponCreateModel, db_session = Depends(get_db_session)):
    return create_coupon_(model, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[CouponResponseModel|None])
async def get_coupon_by_id(id: str, db_session = Depends(get_db_session)):
    return get_coupon_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[CouponResponseModel|None])
async def update_coupon(id: str, model: CouponUpdateModel, db_session = Depends(get_db_session)):
    return update_coupon_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[bool])
async def delete_coupon(id: str, db_session = Depends(get_db_session)):
    return delete_coupon_(id, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[CouponSearchResults|None])
async def search_coupons(
        query_params: CouponSearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = CouponSearchFilter(**query_params.dict())
    return search_coupons_(filter, db_session)