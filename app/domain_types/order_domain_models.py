from typing import Optional, List
from pydantic import UUID4, BaseModel, Field
from datetime import datetime

from app.domain_types.base_search_types import BaseSearchFilter, BaseSearchResults

class OrderCreateModel(BaseModel):
    OrderTypeId: UUID4 = Field(default=None, Optional=True)
    CustomerId: UUID4 = Field(default=None, Optional=False)
    CartId: UUID4 = Field(default=None, Optional=True)
    TipApplicable: bool = Field(default=False, Optional=False)
    Notes: str = Field(default=None, Optional=True)
    OrderLineItems: list = Field(default=[], Optional=True)
    CouponId: UUID4 = Field(default=None, Optional=True)

# Please note that -
# CustomerId, OrderLineItems, OrderStatus cannot be updated through regular update API.
# CustomerId is set when the order is created.
# Order Status is updated through a different set of APIs.
# OrderLineItems are updated through a different set of APIs.

class OrderUpdateModel(BaseModel):
    OrderTypeId: UUID4 = Field(default=None, Optional=True)
    CartId: UUID4 = Field(default=None, Optional=True)
    OrderDiscount: float = Field(Optional=True)
    TipApplicable: bool = Field(Optional=True)
    TipAmount: float = Field(Optional=True)
    Notes: str = Field(default=None, Optional=True)
    CouponId: UUID4 = Field(default=None, Optional=True)
    PaymentTransactionId: UUID4 = Field(default=None, Optional=True)
    RefundTransactionId: UUID4 = Field(default=None, Optional=True)

class OrderSearchFilter(BaseSearchFilter):
    CustomerId: UUID4 = Field(Optional=True)
    CartId: UUID4 = Field(Optional=True)
    TotalItemsCountGreaterThan: int = Field(Optional=True)
    TotalItemsCountLessThan: int = Field(Optional=True)
    OrderDiscountGreaterThan: float = Field(Optional=True)
    OrderDiscountLessThan: float = Field(Optional=True)
    TipApplicable: bool = Field(Optional=True)
    TotalAmountGreaterThan: float = Field(Optional=True)
    TotalAmountLessThan: float = Field(Optional=True)
    OrderLineItemId: UUID4 = Field(Optional=True)
    CouponId: UUID4 = Field(Optional=True)
    OrderStatus: str = Field(Optional=True)
    OrderType: str = Field(Optional=True)
    CreatedBefore: datetime = Field(Optional=True)
    CreatedAfter: datetime = Field(Optional=True)
    PastMonths: int = Field(Optional=True)

class OrderResponseModel(BaseModel):
    id: UUID4
    DisplayCode: str
    InvoiceNumber: str
    CartId: UUID4
    TotalItemsCount: int
    OrderDiscount: float
    TipApplicable: bool
    TipAmount: float
    TotalTax: float
    TotalDiscount: float
    TotalAmount: float
    Notes: str
    OrderLineItems: List[dict]
    CouponId: UUID4
    Coupon: dict
    PaymentTransaction: dict
    RefundTransactionId: dict
    OrderStatus: str
    OrderType: str
    CreatedAt: datetime
    UpdatedAt: datetime


class OrderSearchResults(BaseSearchResults):
    Items: List[OrderResponseModel] = Field(default=None, Optional=True)
