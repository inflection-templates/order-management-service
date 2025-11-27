import json
from sqlalchemy import Column, DateTime, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.common.utils import generate_uuid4
from app.database.base import Base
from sqlalchemy.sql import func

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, index=True, default=generate_uuid4)
    Name = Column(String(255), nullable=False)
    Code = Column(String(50), unique=True, nullable=False)  # Used for identification
    Description = Column(Text, nullable=True)
    Domain = Column(String(255), nullable=True)
    Industry = Column(String(255), nullable=True)
    WebsiteUrl = Column(String(512), nullable=True)
    LogoUrl = Column(String(512), nullable=True)
    ContactEmail = Column(String(512), nullable=True)
    ContactPhone = Column(String(64), nullable=True)
    Address = Column(Text, nullable=True)
    City = Column(String(255), nullable=True)
    State = Column(String(255), nullable=True)
    PostalCode = Column(String(50), nullable=True)
    Country = Column(String(255), nullable=True)
    TenantId = Column(String(36), ForeignKey("tenants.id"), nullable=True)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())
    UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", backref="organizations")

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "Name": self.Name,
            "Code": self.Code,
            "IsActive": self.IsActive,
            "TenantId": self.TenantId
        })

