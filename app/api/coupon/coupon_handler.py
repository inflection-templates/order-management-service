from app.common.utils import validate_uuid4
from app.database.services import coupon_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.coupon import CouponResponseModel, CouponSearchResults
from app.telemetry.tracing import trace_span

@trace_span("handler: create_coupon")
def create_coupon_(model, db_session):
    try:
        coupon = coupon_service.create_coupon(db_session, model)
        message = "Coupon created successfully"
        resp = ResponseModel[CouponResponseModel](Message=message, Data=coupon)
        # print_colorized_json(model)
        return resp

    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: get_coupon_by_id")
def get_coupon_by_id_(id, db_session):
    try:
        coupon_id = validate_uuid4(id)
        customer = coupon_service.get_customer_by_id(db_session, coupon_id)
        message = "Coupon retrieved successfully"
        resp = ResponseModel[CouponResponseModel](Message=message, Data=customer)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()


@trace_span("handler: update_coupon")
def update_coupon_(id, model, db_session):
    try:
        coupon_id = validate_uuid4(id)
        coupon = coupon_service.update_coupon(db_session, coupon_id, model)
        message = "Coupon updated successfully"
        resp = ResponseModel[CouponResponseModel](Message=message, Data=coupon)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: delete_coupon")
def delete_coupon_(id, db_session):
    try:
        coupon_id = validate_uuid4(id)
        coupon = coupon_service.delete_coupon(db_session, coupon_id)
        message = "Coupon deleted successfully"
        resp = ResponseModel[bool](Message=message, Data=coupon)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()

@trace_span("handler: search_coupons")
def search_coupons_(filter, db_session):
    try:
        coupons = coupon_service.search_coupons(db_session, filter)
        message = "Coupons retrieved successfully"
        resp = ResponseModel[CouponSearchResults](Message=message, Data=coupons)
        # print_colorized_json(model)
        return resp
    except Exception as e:
        db_session.rollback()
        db_session.close()
        raise e
    finally:
        db_session.close()