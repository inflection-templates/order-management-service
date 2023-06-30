from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class OrderLineItemCreateModel(BaseModel):
    Name              : str       = Field(description="Name of Item")
    CatalogId         : str       = Field(default=None, description="Catalogue Id of Item")
    Quantity          : int       = Field(description="Quantity of Items")
    UnitPrice         : float     = Field(description="Price of Item per unit")
    Discount          : float     = Field(default=None, description="Discount on Item")
    DiscountSchemeId  : str       = Field(default=None, description="Id of discount scheme applied")
    Tax               : float     = Field(description="Total tax on Items")
    ItemSubTotal      : float     = Field(description="Total amount of Item")
    OrderId           : str       = Field(description="Id of order the items belong to")
    CartId            : str       = Field(description="Id of cart the items belong to")

class OrderLineItemUpdateModel(BaseModel):
    Name              : Optional[str]       = Field(description="Name of Item")
    Quantity          : Optional[int]       = Field(description="Quantity of Items")
    UnitPrice         : Optional[float]     = Field(description="Price of Item per unit")
    Discount          : Optional[float]     = Field(description="Discount on Item")
    DiscountSchemeId  : Optional[str]       = Field(description="Id of discount scheme applied")
    Tax               : Optional[float]     = Field(description="Total tax on Items")
    ItemSubTotal      : Optional[float]     = Field(description="Total amount of Item")
    OrderId           : Optional[str]       = Field(description="Id of order the items belong to")
    CartId            : Optional[str]       = Field(description="Id of cart the items belong to")

class OrderLineItemSearchFilter(BaseSearchFilter):
    Name              : Optional[str]       = Field(description="Search by Name of Item")
    CatalogId         : Optional[str]       = Field(description="Search by Catalogue Id of Item")
    DiscountSchemeId  : Optional[str]       = Field(description="Search by id of discount scheme applied")
    ItemSubTotal      : Optional[float]     = Field(description="Sarch by total amount of Item")
    OrderId           : Optional[str]       = Field(description="Search by order id")
    CartId            : Optional[str]       = Field(description="Search by cart id")
    CreatedBefore     : Optional[datetime]  = Field(description="Search order line items created before the given date")
    CreatedAfter      : Optional[datetime]  = Field(description="Search order line items created after the given date")

class OrderLineItemResponseModel(BaseModel):
    id                : UUID4     = Field(description="Id of Item")
    Name              : str       = Field(description="Name of Item")
    CatalogId         : str       = Field(default=None, description="Catalogue Id of Item")
    Quantity          : int       = Field(description="Quantity of Items")
    UnitPrice         : float     = Field(description="Price of Item per unit")
    Discount          : float     = Field(default=None, description="Discount on Item")
    DiscountSchemeId  : str       = Field(default=None, description="Id of discount scheme applied")
    Tax               : float     = Field(description="Total tax on Items")
    ItemSubTotal      : float     = Field(description="Total amount of Item")
    OrderId           : str       = Field(description="Id of order the items belong to")
    CartId            : str       = Field(description="Id of cart the items belong to")
    CreatedAt         : datetime  = Field(default=datetime.now(), description="Order creation date")
    UpdatedAt         : datetime  = Field(default=datetime.now(), description="Order last updated date")

class OrderLineItemSearchResults(BaseSearchResults):
    Items: List[OrderLineItemResponseModel] = Field(default=[])
