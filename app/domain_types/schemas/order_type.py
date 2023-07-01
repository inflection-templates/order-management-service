from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class OrderTypeCreateModel(BaseModel):
    Name         : str
    Description  : str | None

class OrderTypeUpdateModel(BaseModel):
    Name         : Optional[str]
    Description  : Optional[str | None]

class OrderTypeSearchFilter(BaseSearchFilter):
    Name         : Optional[str]
    Description  : Optional[str | None]

class OrderTypeResponseModel(BaseModel):
    id          : UUID4          = Field(description="Id of order type")
    Name        : str            = Field(description="Name of order type")
    Description : str            = Field(description="Description of order type")
    CreatedAt   : datetime       = Field(default=datetime.now())
    UpdatedAt   : datetime       = Field(default=datetime.now())

class OrderSearchResults(BaseSearchResults):
    Items: List[OrderTypeResponseModel] = Field(default=[])

