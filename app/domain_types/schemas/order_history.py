from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults
from app.domain_types.enums.order_status_types import OrderStatusTypes

class OrderHistoryCreateModel(BaseModel):
    OrderId         : str                       = Field(description="Id of order")
    PreviousStatus  : OrderStatusTypes          = Field(default=OrderStatusTypes.DRAFT.value, description="Previous status of order")
    Status          : OrderStatusTypes          = Field(default=OrderStatusTypes.DRAFT.value, description="Current status of order")
    UpdatedByUserId : str                       = Field(description="Id of user")
    Timestamp       = datetime                  = Field(description="Date and time of order")

class OrderHistoryUpdateModel(BaseModel):
    OrderId         : Optional[str]                       = Field(description="Id of order")
    PreviousStatus  : Optional[OrderStatusTypes]          = Field(description="Previous status of order")
    Status          : Optional[OrderStatusTypes]          = Field(description="Current status of order")
    UpdatedByUserId : Optional[str]                       = Field(description="Id of user")
    Timestamp       : Optional[datetime]                  = Field(description="Date and time of order")

class OrderHistorySearchFilter(BaseSearchFilter):
    OrderId         : Optional[str]                       = Field(description="Id of order")
    PreviousStatus  : Optional[OrderStatusTypes]          = Field(description="Previous status of order")
    Status          : Optional[OrderStatusTypes]          = Field(description="Current status of order")
    UpdatedByUserId : Optional[str]                       = Field(description="Id of user")
    Timestamp       : Optional[datetime]                  = Field(description="Date and time of order")

class OrderHistoryResponseModel(BaseModel):
    id              : UUID4                                      = Field(description="Id of order history")
    OrderId         : str                                        = Field(description="Id of order")
    PreviousStatus  : Optional[OrderStatusTypes | None]          = Field(description="Previous status of order")
    Status          : Optional[OrderStatusTypes | None]          = Field(description="Current status of order")
    UpdatedByUserId : Optional[str]                              = Field(description="Id of user")
    Timestamp       : Optional[datetime]                         = Field(description="Date and time of order")

class OrderHistorySearchResults(BaseSearchResults):
    Items: List[OrderHistoryResponseModel] = Field(default=[])

