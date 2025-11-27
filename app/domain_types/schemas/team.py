import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults

class TeamCreateModel(BaseModel):
    Name: str = Field(min_length=1, max_length=255, description="Name of the team")
    Code: str = Field(min_length=1, max_length=50, description="Unique code for the team")
    Description: Optional[str | None] = Field(default=None, description="Description of the team")
    OrganizationId: Optional[str | None] = Field(default=None, description="Organization ID associated with the team")
    OwnerUserId: Optional[str | None] = Field(default=None, description="Owner user ID of the team")
    Permissions: Optional[List[str] | None] = Field(default=None, description="List of permissions for the team")
    IsActive: Optional[bool] = Field(default=True, description="Whether the team is active")

TeamCreateModel.model_rebuild()

class TeamUpdateModel(BaseModel):
    Name: Optional[str | None] = Field(default=None, min_length=1, max_length=255, description="Name of the team")
    Code: Optional[str | None] = Field(default=None, min_length=1, max_length=50, description="Unique code for the team")
    Description: Optional[str | None] = Field(default=None, description="Description of the team")
    OrganizationId: Optional[str | None] = Field(default=None, description="Organization ID associated with the team")
    OwnerUserId: Optional[str | None] = Field(default=None, description="Owner user ID of the team")
    Permissions: Optional[List[str] | None] = Field(default=None, description="List of permissions for the team")
    IsActive: Optional[bool] = Field(default=None, description="Whether the team is active")

TeamUpdateModel.model_rebuild()

class TeamResponseModel(BaseModel):
    id: str
    Name: str
    Code: str
    Description: Optional[str | None]
    OrganizationId: Optional[str | None]
    OwnerUserId: Optional[str | None]
    Permissions: Optional[List[str] | None]
    IsActive: bool
    CreatedAt: datetime.datetime
    UpdatedAt: datetime.datetime

TeamResponseModel.model_rebuild()

class TeamSearchFilter(BaseSearchFilter):
    Name: Optional[str | None] = Field(default=None, description="Name of the team")
    Code: Optional[str | None] = Field(default=None, description="Code of the team")
    OrganizationId: Optional[str | None] = Field(default=None, description="Organization ID of the team")
    OwnerUserId: Optional[str | None] = Field(default=None, description="Owner user ID of the team")
    IsActive: Optional[bool] = Field(default=None, description="Whether the team is active")

TeamSearchFilter.model_rebuild()

class TeamSearchResults(BaseSearchResults):
    Items: List[TeamResponseModel] = Field(description="List of teams")

TeamSearchResults.model_rebuild()

