from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.order_status_types import OrderStatusTypes
from app.domain_types.base_search_types import BaseSearchFilter, BaseSearchResults

class OrderCreateModel(BaseModel):
      OrderTypeId    : Optional[UUID4 | None] = Field(default=None)
      CustomerId     : UUID4                  = Field(...)
      CartId         : Optional[UUID4 | None] = Field(default=None)
      TipApplicable  : Optional[bool | None]  = Field(default=False)
      Notes          : Optional[str | None]   = Field(default=None, min_length=5, max_length=1024)
      OrderLineItems : Optional[list]         = Field(default=[])
      CouponId       : Optional[UUID4 | None] = Field(default=None)

# Please note that -
# CustomerId, OrderLineItems, OrderStatus cannot be updated through regular update API.
# CustomerId is set when the order is created.
# Order Status is updated through a different set of APIs.
# OrderLineItems are updated through a different set of APIs.

class OrderUpdateModel(BaseModel):
    OrderTypeId         : Optional[UUID4]
    CartId              : Optional[UUID4]
    OrderDiscount       : Optional[float] = Field(ge=0.0)
    TipApplicable       : Optional[bool]
    TipAmount           : Optional[float] = Field(ge=0.0)
    Notes               : Optional[str]   = Field(min_length=5, max_length=1024)
    CouponId            : Optional[UUID4]
    PaymentTransactionId: Optional[UUID4]
    RefundTransactionId : Optional[UUID4]

class OrderSearchFilter(BaseSearchFilter):
    CustomerId                : Optional[UUID4]
    CartId                    : Optional[UUID4]
    TotalItemsCountGreaterThan: Optional[int]      = Field(ge=0, le=100)
    TotalItemsCountLessThan   : Optional[int]      = Field(ge=1, le=100)
    OrderDiscountGreaterThan  : Optional[float]    = Field(ge=0.0)
    OrderDiscountLessThan     : Optional[float]    = Field(ge=0.0)
    TipApplicable             : Optional[bool]
    TotalAmountGreaterThan    : Optional[float]    = Field(ge=0.0)
    TotalAmountLessThan       : Optional[float]    = Field(ge=0.0)
    OrderLineItemId           : Optional[UUID4]
    CouponId                  : Optional[UUID4]
    OrderStatus               : Optional[OrderStatusTypes]
    OrderType                 : Optional[str]      = Field(min_length=2, max_length=64)
    CreatedBefore             : Optional[datetime]
    CreatedAfter              : Optional[datetime]
    PastMonths                : Optional[int]      = Field(ge=0, le=12)

class OrderResponseModel(BaseModel):
    id                 : UUID4
    DisplayCode        : str
    InvoiceNumber      : str
    CartId             : UUID4
    TotalItemsCount    : int
    OrderDiscount      : float
    TipApplicable      : bool
    TipAmount          : float
    TotalTax           : float
    TotalDiscount      : float
    TotalAmount        : float
    Notes              : str
    OrderLineItems     : List[dict]
    CouponId           : UUID4
    Coupon             : dict
    PaymentTransaction : dict
    RefundTransactionId: dict
    OrderStatus        : str
    OrderType          : str
    CreatedAt          : datetime
    UpdatedAt          : datetime


class OrderSearchResults(BaseSearchResults):
    Items: List[OrderResponseModel] = Field(default=[])
