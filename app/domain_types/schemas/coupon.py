from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.enums.discount_type import DiscountTypes
from app.domain_types.enums.order_status_types import OrderStatusTypes
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class CouponCreateModel(BaseModel):
    Name               : str           = Field(..., min_length=2, max_length=64)
    Description        : str           = Field(..., min_length=2, max_length=1024)
    CouponCode         : str           = Field(..., min_length=2, max_length=64)
    CouponType         : str           = Field(..., min_length=2, max_length=64)
    Discount           : float         = Field(default=0, ge=0.0)
    DiscountType       : DiscountTypes = Field(default=DiscountTypes.FLAT)
    DiscountPercentage : float         = Field(default=0.0, ge=0.0, le=100.0)
    DiscountMaxAmount  : float         = Field(default=0.0, ge=0.0)
    StartDate          : datetime      = Field(default=datetime.now())
    EndDate            : datetime      = Field(default=None)
    MaxUsage           : int           = Field(default=1000, ge=0, le=10000)
    MaxUsagePerUser    : int           = Field(default=1, ge=0, le=10)
    MaxUsagePerOrder   : int           = Field(default=1, ge=0, le=5)
    MinOrderAmount     : float         = Field(default=100, ge=0.0)
    IsActive           : bool          = Field(default=True)
    IsDeleted          : bool          = Field(default=False)
    CreatedBy          : UUID4         = Field(default=None)

class CouponUpdateModel(BaseModel):
    Name               : Optional[str]           = Field(..., min_length=2, max_length=64)
    Description        : Optional[str]           = Field(..., min_length=2, max_length=1024)
    CouponCode         : Optional[str]           = Field(..., min_length=2, max_length=64)
    CouponType         : Optional[str]           = Field(..., min_length=2, max_length=64)
    Discount           : Optional[float]         = Field(default=0, ge=0.0)
    DiscountType       : Optional[DiscountTypes] = Field(default=DiscountTypes.FLAT)
    DiscountPercentage : Optional[float]         = Field(default=0.0, ge=0.0, le=100.0)
    DiscountMaxAmount  : Optional[float]         = Field(default=0.0, ge=0.0)
    StartDate          : Optional[datetime]      = Field(default=datetime.now())
    EndDate            : Optional[datetime]      = Field(default=None)
    MaxUsage           : Optional[int]           = Field(default=1000, ge=0, le=10000)
    MaxUsagePerUser    : Optional[int]           = Field(default=1, ge=0, le=10)
    MaxUsagePerOrder   : Optional[int]           = Field(default=1, ge=0, le=5)
    MinOrderAmount     : Optional[float]         = Field(default=100, ge=0.0)
    IsActive           : Optional[bool]          = Field(default=True)
    IsDeleted          : Optional[bool]          = Field(default=False)

class CouponSearchFilter(BaseSearchFilter):
    Name               : Optional[str]           = Field(description="Search coupon by name")
    CouponCode         : Optional[str]           = Field(description="Search coupon by coupon code")
    StartDate          : Optional[datetime]      = Field(description="Search coupon by start date")
    Discount           : Optional[float]         = Field(description="Search coupon by discount")
    DiscountType       : Optional[DiscountTypes] = Field(description="Search coupon by discount type")
    DiscountPercentage : Optional[float]         = Field(description="Search coupon by discount percentage")
    MinOrderAmount     : Optional[float]         = Field(description="Search coupon by minimum order amount")
    IsActive           : Optional[bool]          = Field(description="Search coupon by its state")

class CouponResponseModel(BaseModel):
    id
    Name               : UUID4         = Field(description="Id of the coupon")
    Description        : str           = Field(description="Description of coupon")
    CouponCode         : str           = Field(description="Code of coupon")
    CouponType         : str           = Field(description="Type of coupon")
    Discount           : float         = Field(default=0, ge=0.0, description="Coupon discount")
    DiscountType       : DiscountTypes = Field(default=DiscountTypes.FLAT, description="Type of discount")
    DiscountPercentage : float         = Field(description="Percentage of discount")
    DiscountMaxAmount  : float         = Field(description="Max amount of discount")
    StartDate          : datetime      = Field(description="Start date of coupon discount")
    EndDate            : datetime      = Field(default=None, description="End date of coupon discount")
    MaxUsage           : int           = Field(default=1000, description="Max usage of coupon")
    MaxUsagePerUser    : int           = Field(default=1, description="Max usage of coupon per user")
    MaxUsagePerOrder   : int           = Field(default=1, description="Max usage of coupon per order")
    MinOrderAmount     : float         = Field(default=100, description="Minimum order amount to use this coupon")
    IsActive           : bool          = Field(default=True, description="Coupon is active or not")
    IsDeleted          : bool          = Field(default=False, description="Coupon is deleted or not")
    CreatedBy          : UUID4         = Field(default=None, description="Id of coupon creator")
    CreatedAt          : datetime      = Field(description="Created at")
    UpdatedAt          : datetime      = Field(description="Updated at")

class CouponSearchResults(BaseSearchResults):
    Items : List[CouponResponseModel] = Field(description="List of coupons")

