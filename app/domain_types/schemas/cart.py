from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.enums.order_status_types import OrderStatusTypes
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class CartCreateModel(BaseModel):
    CustomerId: UUID4 = Field(...)
    # CartLineItems: Optional[list] = Field(default=[])
    AssociatedOrderId   : Optional[str] = Field(...)
    CartToOrderTimestamp: Optional[datetime] = Field(...)
    TotalItemsCount     : Optional[int] = Field(...)
    TotalAmount         : Optional[float] = Field(...)

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
    # CartLineItems       : list
    Discount            : float | None
    TotalTax            : float | None
    TotalDiscount       : float | None
    TotalItemsCount     : int | None
    TotalAmount         : float | None
    AssociatedOrderId   : UUID4
    CartToOrderTimestamp: datetime | None
    CreatedAt           : datetime
    UpdatedAt           : datetime

class CartSearchResults(BaseSearchResults):
    Items: List[CartResponseModel] = []

