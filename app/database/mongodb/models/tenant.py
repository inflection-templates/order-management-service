from typing import Optional
from pydantic import BaseModel, Field
from app.database.mongodb.models.base_model import MongoDBBaseModel

class TenantModel(MongoDBBaseModel):
    """MongoDB model for tenants"""
    
    name: str = Field(..., description="Tenant name")
    domain: Optional[str] = Field(None, description="Tenant domain")
    is_active: bool = Field(default=True, description="Whether the tenant is active")
    settings: dict = Field(default_factory=dict, description="Tenant-specific settings")