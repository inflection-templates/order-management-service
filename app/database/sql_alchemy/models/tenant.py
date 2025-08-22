import json
from sqlalchemy import Column, DateTime, String, Boolean, Text
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.sql_alchemy.base import Base
from sqlalchemy.sql import func

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    Name = Column(String(255), nullable=False)
    Code = Column(String(50), unique=True, nullable=False)  # Used for subdomain/identification
    Description = Column(Text, nullable=True)
    IsActive = Column(Boolean, default=True)
    IsDefault = Column(Boolean, default=False)  # For system users
    Settings = Column(Text, nullable=True)  # JSON settings for tenant-specific configurations
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    users = relationship("User", back_populates="tenant")

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "Name": self.Name,
            "Code": self.Code,
            "IsActive": self.IsActive,
            "IsDefault": self.IsDefault
        })
