from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.enums.order_status_types import OrderStatusTypes
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class OrderCreateModel(BaseModel):
      OrderTypeId    : Optional[UUID4 | None] = Field(default=None, description="Id of the order type")
      CustomerId     : UUID4                  = Field(description="Id of the customer")
      CartId         : Optional[UUID4 | None] = Field(default=None, description="Id of the cart")
      TipApplicable  : Optional[bool | None]  = Field(default=False, description="Tip applicable or not")
      Notes          : Optional[str | None]   = Field(default=None, min_length=5, max_length=1024, description="Notes for the delivery")
      OrderLineItems : Optional[list]         = Field(default=[], description="List of order line items")

# Please note that -
# CustomerId, OrderLineItems, OrderStatus cannot be updated through regular update API.
# CustomerId is set when the order is created.
# Order Status is updated through a different set of APIs.
# OrderLineItems are updated through a different set of APIs.

class OrderUpdateModel(BaseModel):
    OrderTypeId          : Optional[UUID4] = Field(description="Id of the order type")
    CartId               : Optional[UUID4] = Field(description="Id of the cart")
    OrderDiscount        : Optional[float] = Field(ge=0.0, description="Discount applied to the order")
    TipApplicable        : Optional[bool]  = Field(description="Tip applicable or not")
    TipAmount            : Optional[float] = Field(ge=0.0, description="Tip amount")
    Notes                : Optional[str]   = Field(min_length=5, max_length=1024, description="Notes for the delivery")
    PaymentTransactionId : Optional[UUID4] = Field(description="Id of the payment transaction")
    RefundTransactionId  : Optional[UUID4] = Field(description="Id of the refund transaction")

class OrderSearchFilter(BaseSearchFilter):
    CustomerId                 : Optional[UUID4]            = Field(description="Search by the Id of the customer")
    CartId                     : Optional[UUID4]            = Field(description="Search by the associated cart Id")
    CouponId                   : Optional[UUID4]            = Field(description="Search by the applied coupon Id")
    TotalItemsCountGreaterThan : Optional[int]              = Field(ge=0, le=100, description="Search orders with total items greater than given value")
    TotalItemsCountLessThan    : Optional[int]              = Field(ge=1, le=100, description="Search orders with total items less than given value")
    OrderDiscountGreaterThan   : Optional[float]            = Field(ge=0.0, description="Search orders with discount applied to the order greater than this value")
    OrderDiscountLessThan      : Optional[float]            = Field(ge=0.0, description="Search orders with discount applied to the order less than this value")
    TipApplicable              : Optional[bool]             = Field(description="Search orders with tip applicable or not")
    TotalAmountGreaterThan     : Optional[float]            = Field(ge=0.0, description="Search orders with total amount greater than this value")
    TotalAmountLessThan        : Optional[float]            = Field(ge=0.0, description="Search orders with total amount less than this value")
    OrderLineItemProductId     : Optional[UUID4]            = Field(description="Search orders with the given order line item's product Id")
    OrderStatus                : Optional[OrderStatusTypes] = Field(description="Search orders with the given order status")
    OrderType                  : Optional[str]              = Field(min_length=2, max_length=64, description="Search orders with the given order type")
    CreatedBefore              : Optional[datetime]         = Field(description="Search orders created before the given date")
    CreatedAfter               : Optional[datetime]         = Field(description="Search orders created after the given date")
    PastMonths                 : Optional[int]              = Field(ge=0, le=12, description="Search orders created in the past given number of months")

class OrderResponseModel(BaseModel):
    id                  : UUID4                       = Field(description="Id of the order")
    DisplayCode         : str                         = Field(min_length=4, max_length=64, description="Display code for the order")
    InvoiceNumber       : str | None                  = Field(default=None, description="Invoice number for the order")
    CartId              : UUID4 | None                = Field(default=None, description="Cart Id for the order")
    TotalItemsCount     : int                         = Field(ge=0, le=100, default=0, description="Total items in the order")
    OrderDiscount       : float                       = Field(ge=0.0, default=0.0, description="Discount applied to the order")
    TipApplicable       : bool                        = Field(default=False, description="Is tip applicable for the order")
    TipAmount           : float                       = Field(ge=0.0, default=0.0, description="Tip amount for the order")
    TotalTax            : float                       = Field(ge=0.0, default=0.0, description="Total tax for the order")
    TotalDiscount       : float                       = Field(ge=0.0, default=0.0, description="Total discount for the order")
    TotalAmount         : float                       = Field(ge=0.0, default=0.0, description="Total amount for the order")
    Notes               : str | None                  = Field(min_length=5, max_length=1024, default=None, description="Notes added for the order for the delivery")
    OrderLineItems      : List[dict] | None           = Field(default=None, description="Order line items")
    Coupons             : Optional[List[dict] | None] = Field(default=None, description="Coupons applied to the order")
    PaymentTransaction  : Optional[dict | None]       = Field(default=None, description="Payment transaction details for the order")
    RefundTransactionId : Optional[dict | None]       = Field(default=None, description="Refund transaction details for the order")
    OrderStatus         : OrderStatusTypes            = Field(default=OrderStatusTypes.DRAFT, description="Order status")
    OrderType           : Optional[str | None]        = Field(min_length=2, max_length=64, default=None, description="Order type")
    CreatedAt           : Optional[datetime]          = Field(default=None, description="Order creation date")
    UpdatedAt           : Optional[datetime]          = Field(default=None, description="Order last updated date")


class OrderSearchResults(BaseSearchResults):
    Items: List[OrderResponseModel] = Field(default=[])
