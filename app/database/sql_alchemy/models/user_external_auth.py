import json
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from app.common.utils import generate_uuid4
from app.database.sql_alchemy.base import Base
from sqlalchemy.sql import func

class UserExternalAuth(Base):
    __tablename__ = "user_external_auths"

    id = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    UserId = Column(String(36), ForeignKey("users.id"), nullable=False)
    Provider = Column(String(50), nullable=False)  # google, facebook, github, twitter, gitlab, cognito, azure_ad, saml
    ExternalUserId = Column(String(255), nullable=False)
    Email = Column(String(512), nullable=True)
    DisplayName = Column(String(255), nullable=True)
    AccessToken = Column(Text, nullable=True)
    RefreshToken = Column(Text, nullable=True)
    TokenExpiresAt = Column(DateTime(timezone=True), nullable=True)
    AdditionalData = Column(Text, nullable=True)  # JSON for provider-specific data
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "UserId": self.UserId,
            "Provider": self.Provider,
            "ExternalUserId": self.ExternalUserId,
            "Email": self.Email,
            "DisplayName": self.DisplayName
        })
