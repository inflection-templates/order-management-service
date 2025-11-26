import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class TenantCreateModel(BaseModel):
    Name: str = Field(min_length=1, max_length=255, description="Name of the tenant")
    Code: str = Field(min_length=1, max_length=50, description="Unique code for the tenant")
    Description: Optional[str | None] = Field(default=None, description="Description of the tenant")
    IsActive: Optional[bool] = Field(default=True, description="Whether the tenant is active")
    IsDefault: Optional[bool] = Field(default=False, description="Whether this is the default tenant")
    Settings: Optional[str | None] = Field(default=None, description="JSON settings for tenant-specific configurations")

TenantCreateModel.model_rebuild()

class TenantUpdateModel(BaseModel):
    Name: Optional[str | None] = Field(default=None, min_length=1, max_length=255, description="Name of the tenant")
    Code: Optional[str | None] = Field(default=None, min_length=1, max_length=50, description="Unique code for the tenant")
    Description: Optional[str | None] = Field(default=None, description="Description of the tenant")
    IsActive: Optional[bool] = Field(default=None, description="Whether the tenant is active")
    IsDefault: Optional[bool] = Field(default=None, description="Whether this is the default tenant")
    Settings: Optional[str | None] = Field(default=None, description="JSON settings for tenant-specific configurations")

TenantUpdateModel.model_rebuild()

class TenantResponseModel(BaseModel):
    id: str
    Name: str
    Code: str
    Description: Optional[str | None]
    IsActive: bool
    IsDefault: bool
    Settings: Optional[str | None]
    CreatedAt: datetime.datetime
    UpdatedAt: datetime.datetime

TenantResponseModel.model_rebuild()

class TenantSearchFilter(BaseSearchFilter):
    Name: Optional[str | None] = Field(default=None, description="Name of the tenant")
    Code: Optional[str | None] = Field(default=None, description="Code of the tenant")
    IsActive: Optional[bool] = Field(default=None, description="Whether the tenant is active")

TenantSearchFilter.model_rebuild()

class TenantSearchResults(BaseSearchResults):
    Items: List[TenantResponseModel] = Field(description="List of tenants")

TenantSearchResults.model_rebuild()

