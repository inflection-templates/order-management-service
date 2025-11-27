import json
from sqlalchemy import Column, DateTime, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func

class Team(Base):
    __tablename__ = "teams"

    id = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    Name = Column(String(255), nullable=False)
    Code = Column(String(50), unique=True, nullable=False)  # Used for identification
    Description = Column(Text, nullable=True)
    OrganizationId = Column(String(36), ForeignKey("organizations.id"), nullable=True)
    OwnerUserId = Column(String(36), ForeignKey("users.id"), nullable=True)
    Permissions = Column(Text, nullable=True)  # JSON array of permissions
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", backref="teams")
    owner = relationship("User", backref="owned_teams")

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "Name": self.Name,
            "Code": self.Code,
            "IsActive": self.IsActive,
            "OrganizationId": self.OrganizationId,
            "OwnerUserId": self.OwnerUserId
        })

