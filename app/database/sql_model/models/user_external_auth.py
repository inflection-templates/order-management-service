import json
from sqlmodel import SQLModel, Field, Column, DateTime, Text
from app.common.utils import generate_uuid4
from typing import Optional
from datetime import datetime
from sqlalchemy import func

class UserExternalAuth(SQLModel, table=True):
    __tablename__ = "user_external_auths"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    UserId: str = Field(foreign_key="users.id", max_length=36)
    Provider: str = Field(max_length=50)  # google, facebook, github, twitter, gitlab, cognito, azure_ad, saml
    ExternalUserId: str = Field(max_length=255)
    Email: Optional[str] = Field(default=None, max_length=512)
    DisplayName: Optional[str] = Field(default=None, max_length=255)
    AccessToken: Optional[str] = Field(default=None, sa_column=Column(Text))
    RefreshToken: Optional[str] = Field(default=None, sa_column=Column(Text))
    TokenExpiresAt: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    AdditionalData: Optional[str] = Field(default=None, sa_column=Column(Text))  # JSON for provider-specific data
    CreatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "UserId": self.UserId,
            "Provider": self.Provider,
            "ExternalUserId": self.ExternalUserId,
            "Email": self.Email,
            "DisplayName": self.DisplayName
        })
