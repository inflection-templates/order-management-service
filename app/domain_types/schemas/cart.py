from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.enums.order_status_types import OrderStatusTypes
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class CartCreateModel(BaseModel):
    CustomerId: UUID4 = Field(...)
    CartLineItems: Optional[list] = Field(default=[])

class CartUpdateModel(BaseModel):
    pass

class CartSearchFilter(BaseSearchFilter):
    CustomerId                : Optional[UUID4]
    ProductId                 : Optional[UUID4]
    TotalItemsCountGreaterThan: Optional[int] = Field(ge=0, le=100)
    TotalItemsCountLessThan   : Optional[int] = Field(ge=1, le=100)
    TotalAmountGreaterThan    : Optional[float] = Field(ge=0.0)
    TotalAmountLessThan       : Optional[float] = Field(ge=0.0)
    CreatedBefore             : Optional[datetime]
    CreatedAfter              : Optional[datetime]

class CartResponseModel(BaseModel):
    id                  : UUID4
    CustomerId          : UUID4
    CartLineItems       : list
    Discount            : float
    TotalTax            : float
    TotalDiscount       : float
    TotalItemsCount     : int
    TotalAmount         : float
    AssociatedOrderId   : UUID4
    CartToOrderTimestamp: datetime
    CreatedAt           : datetime
    UpdatedAt           : datetime

class CartSearchResults(BaseSearchResults):
    Items: List[CartResponseModel] = []

