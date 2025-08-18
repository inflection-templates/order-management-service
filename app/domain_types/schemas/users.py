from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, Field
from app.domain_types.schemas.base_search_types import BaseSearchFilter, BaseSearchResults
from app.domain_types.schemas.base_validation import StrictBaseModel


class UserCreateModel(StrictBaseModel):
    FirstName: str = Field(..., min_length=1, max_length=64, description="User's first name")
    LastName: str = Field(..., min_length=1, max_length=64, description="User's last name")
    UserName: str = Field(..., min_length=3, max_length=32, description="Unique username")
    Email: str = Field(..., min_length=5, max_length=255, description="User's email address")
    CountryCode: str = Field(..., min_length=1, max_length=5, description="Country calling code")
    PhoneNumber: str = Field(..., min_length=7, max_length=15, description="User's phone number")
    Password: str = Field(..., min_length=8, max_length=128, description="User's password")


class UserUpdateModel(StrictBaseModel):
    FirstName: Optional[str] = Field(None, min_length=1, max_length=64, description="User's first name")
    LastName: Optional[str] = Field(None, min_length=1, max_length=64, description="User's last name")
    UserName: Optional[str] = Field(None, min_length=3, max_length=32, description="Unique username")
    Email: Optional[str] = Field(None, min_length=5, max_length=255, description="User's email address")
    CountryCode: Optional[str] = Field(None, min_length=1, max_length=5, description="Country calling code")
    PhoneNumber: Optional[str] = Field(None, min_length=7, max_length=15, description="User's phone number")
    Password: Optional[str] = Field(None, min_length=8, max_length=128, description="User's password")


class UserSearchFilter(BaseSearchFilter):
    FirstName: Optional[str] = Field(None, min_length=1, max_length=64, description="User's first name")
    LastName: Optional[str] = Field(None, min_length=1, max_length=64, description="User's last name")
    UserName: Optional[str] = Field(None, min_length=3, max_length=32, description="Username")
    Email: Optional[str] = Field(None, min_length=5, max_length=255, description="User's email address")
    CountryCode: Optional[str] = Field(None, min_length=1, max_length=5, description="Country calling code")


class UserResponseModel(BaseModel):
    id: UUID4 = Field(description="Unique identifier for the User")
    FirstName: str = Field(description="User's first name")
    LastName: str = Field(description="User's last name")
    UserName: str = Field(description="Unique username")
    Email: str = Field(description="User's email address")
    CountryCode: str = Field(description="Country calling code")
    PhoneNumber: str = Field(description="User's phone number")
    created_at: datetime = Field(description="User creation timestamp")
    updated_at: datetime = Field(description="User last update timestamp")

    class Config:
        orm_mode = True


class UserSearchResults(BaseSearchResults):
    Items: List[UserResponseModel] = Field(default_factory=list)


class DeleteResponseModel(BaseModel):
    deleted: bool = Field(description="Indicates if the deletion was successful", default=True)


UserCreateModel.update_forward_refs()
UserUpdateModel.update_forward_refs()
UserSearchFilter.update_forward_refs()
UserResponseModel.update_forward_refs()
UserSearchResults.update_forward_refs()
