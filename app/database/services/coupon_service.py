import datetime as dt
import uuid
# from fastapi import HTTPException, Query, Body
from app.common.utils import print_colorized_json
from app.database.models.coupon import Coupon
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.coupon import CouponCreateModel, CouponResponseModel, CouponUpdateModel, CouponSearchFilter, CouponSearchResults
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.telemetry.tracing import trace_span

@trace_span("service: create_coupon")
def create_coupon(session: Session, model: CouponCreateModel) -> CouponResponseModel:
    model_dict = model.dict()
    db_model = Coupon(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    coupon = db_model

    return coupon.__dict__

@trace_span("service: get_coupon_by_id")
def get_coupon_by_id(session: Session, coupon_id: str) -> CouponResponseModel:
    coupon = session.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise NotFound(f"Coupon with id {coupon_id} not found")
    return coupon.__dict__

@trace_span("service: update_coupon")
def update_coupon(session: Session, coupon_id: str, model: CouponUpdateModel) -> CouponResponseModel:
    coupon = session.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise NotFound(f"Coupon with id {coupon_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Coupon).filter(Coupon.id == coupon_id).update(
        update_data, synchronize_session="auto")

    session.commit()
    session.refresh(coupon)
    return coupon.__dict__

@trace_span("service: delete_coupon")
def delete_coupon(session: Session, coupon_id: str):
    coupon = session.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not coupon:
        raise NotFound(f"Coupon with id {coupon_id} not found")
    session.delete(coupon)
    session.commit()
    return True

@trace_span("service: search_coupons")
def search_coupons(session: Session, filter) -> CouponSearchResults:

    query = session.query(Coupon)
    if filter.Name:
        query = query.filter(Coupon.Name == filter.Name)
    if filter.CouponCode:
        query = query.filter(Coupon.EmailCouponCode == filter.CouponCode)
    if filter.Discount:
        query = query.filter(Coupon.Discount == filter.Discount)
    if filter.DiscountType:
        query = query.filter(Coupon.DiscountType == filter.DiscountType)
    if filter.DiscountPercentage:
        query = query.filter(Coupon.DiscountPercentage == filter.DiscountPercentage)
    if filter.IsActive:
        query = query.filter(Coupon.IsActive == filter.IsActive)
    if filter.StartDate:
        query = query.filter(Coupon.CreatedAt == filter.StartDate)
    if filter.MinOrderAmount:
        query = query.filter(Coupon.MinOrderAmount == filter.MinOrderAmount)
    coupons = query.all()

    results = CouponSearchResults(
        TotalCount=len(coupons),
        ItemsPerPage=filter.ItemsPerPage,
        PageNumber=filter.PageNumber,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=coupons
    )

    return results.__dict__