from typing import Optional, List
from pydantic import Field
from app.database.mongodb.models.base_model import MongoDBBaseModel

class RoleModel(MongoDBBaseModel):
    """MongoDB Role model"""
    Name: str = Field(..., unique=True, max_length=100)
    Description: Optional[str] = Field(None, max_length=500)
    Permissions: List[str] = Field(default=[])
    IsActive: bool = Field(default=True)
    
    class Config:
        collection_name = "roles"
        schema_extra = {
            "example": {
                "Name": "admin",
                "Description": "Administrator role with full access",
                "Permissions": ["read", "write", "delete", "admin"],
                "IsActive": True
            }
        }
