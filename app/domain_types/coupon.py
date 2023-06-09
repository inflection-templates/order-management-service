from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.enums.discount_type import DiscountTypes
from app.domain_types.enums.order_status_types import OrderStatusTypes
from app.domain_types.base_search_types import BaseSearchFilter, BaseSearchResults

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

