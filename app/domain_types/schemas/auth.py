from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.domain_types.schemas.base_validation import StrictBaseModel
from app.domain_types.enums.role_enum import UserRole


class LoginModel(StrictBaseModel):
    Email: str = Field(..., min_length=5, max_length=255, description="User's email address")
    Password: str = Field(..., min_length=8, max_length=128, description="User's password")
    Role: UserRole = Field(..., description="User role (admin or user)")


class LoginResponseModel(BaseModel):
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user_id: str = Field(description="User ID")
    email: str = Field(description="User email")
    role: UserRole = Field(description="User role")
    expires_at: datetime = Field(description="Token expiration time")

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None


LoginModel.update_forward_refs()
LoginResponseModel.update_forward_refs()
TokenData.update_forward_refs()
