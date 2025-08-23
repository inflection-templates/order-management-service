from typing import Optional
from pydantic import Field
from app.database.mongodb.models.base_model import MongoDBBaseModel

class AddressModel(MongoDBBaseModel):
    """MongoDB Address model"""
    CustomerId: str = Field(...)
    AddressType: str = Field(..., max_length=50)  # billing, shipping, etc.
    StreetAddress: str = Field(..., max_length=200)
    City: str = Field(..., max_length=100)
    State: str = Field(..., max_length=100)
    PostalCode: str = Field(..., max_length=20)
    Country: str = Field(..., max_length=100)
    IsDefault: bool = Field(default=False)
    
    class Config:
        collection_name = "addresses"
        schema_extra = {
            "example": {
                "CustomerId": "customer123",
                "AddressType": "shipping",
                "StreetAddress": "123 Main St",
                "City": "New York",
                "State": "NY",
                "PostalCode": "10001",
                "Country": "USA",
                "IsDefault": True
            }
        }