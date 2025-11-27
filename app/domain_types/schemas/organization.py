import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class OrganizationCreateModel(BaseModel):
    Name: str = Field(min_length=1, max_length=255, description="Name of the organization")
    Code: str = Field(min_length=1, max_length=50, description="Unique code for the organization")
    Description: Optional[str | None] = Field(default=None, description="Description of the organization")
    Domain: Optional[str | None] = Field(default=None, description="Domain of the organization")
    Industry: Optional[str | None] = Field(default=None, description="Industry of the organization")
    WebsiteUrl: Optional[str | None] = Field(default=None, description="Website URL of the organization")
    LogoUrl: Optional[str | None] = Field(default=None, description="Logo URL of the organization")
    ContactEmail: Optional[str | None] = Field(default=None, description="Contact email of the organization")
    ContactPhone: Optional[str | None] = Field(default=None, description="Contact phone of the organization")
    Address: Optional[str | None] = Field(default=None, description="Address of the organization")
    City: Optional[str | None] = Field(default=None, description="City of the organization")
    State: Optional[str | None] = Field(default=None, description="State of the organization")
    PostalCode: Optional[str | None] = Field(default=None, description="Postal code of the organization")
    Country: Optional[str | None] = Field(default=None, description="Country of the organization")
    TenantId: Optional[str | None] = Field(default=None, description="Tenant ID associated with the organization")
    IsActive: Optional[bool] = Field(default=True, description="Whether the organization is active")

OrganizationCreateModel.model_rebuild()

class OrganizationUpdateModel(BaseModel):
    Name: Optional[str | None] = Field(default=None, min_length=1, max_length=255, description="Name of the organization")
    Code: Optional[str | None] = Field(default=None, min_length=1, max_length=50, description="Unique code for the organization")
    Description: Optional[str | None] = Field(default=None, description="Description of the organization")
    Domain: Optional[str | None] = Field(default=None, description="Domain of the organization")
    Industry: Optional[str | None] = Field(default=None, description="Industry of the organization")
    WebsiteUrl: Optional[str | None] = Field(default=None, description="Website URL of the organization")
    LogoUrl: Optional[str | None] = Field(default=None, description="Logo URL of the organization")
    ContactEmail: Optional[str | None] = Field(default=None, description="Contact email of the organization")
    ContactPhone: Optional[str | None] = Field(default=None, description="Contact phone of the organization")
    Address: Optional[str | None] = Field(default=None, description="Address of the organization")
    City: Optional[str | None] = Field(default=None, description="City of the organization")
    State: Optional[str | None] = Field(default=None, description="State of the organization")
    PostalCode: Optional[str | None] = Field(default=None, description="Postal code of the organization")
    Country: Optional[str | None] = Field(default=None, description="Country of the organization")
    TenantId: Optional[str | None] = Field(default=None, description="Tenant ID associated with the organization")
    IsActive: Optional[bool] = Field(default=None, description="Whether the organization is active")

OrganizationUpdateModel.model_rebuild()

class OrganizationResponseModel(BaseModel):
    id: str
    Name: str
    Code: str
    Description: Optional[str | None]
    Domain: Optional[str | None]
    Industry: Optional[str | None]
    WebsiteUrl: Optional[str | None]
    LogoUrl: Optional[str | None]
    ContactEmail: Optional[str | None]
    ContactPhone: Optional[str | None]
    Address: Optional[str | None]
    City: Optional[str | None]
    State: Optional[str | None]
    PostalCode: Optional[str | None]
    Country: Optional[str | None]
    TenantId: Optional[str | None]
    IsActive: bool
    CreatedAt: datetime.datetime
    UpdatedAt: datetime.datetime

OrganizationResponseModel.model_rebuild()

class OrganizationSearchFilter(BaseSearchFilter):
    Name: Optional[str | None] = Field(default=None, description="Name of the organization")
    Code: Optional[str | None] = Field(default=None, description="Code of the organization")
    TenantId: Optional[str | None] = Field(default=None, description="Tenant ID of the organization")
    IsActive: Optional[bool] = Field(default=None, description="Whether the organization is active")

OrganizationSearchFilter.model_rebuild()

class OrganizationSearchResults(BaseSearchResults):
    Items: List[OrganizationResponseModel] = Field(description="List of organizations")

OrganizationSearchResults.model_rebuild()

