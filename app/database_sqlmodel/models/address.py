import datetime
import json
from sqlmodel import Field, SQLModel, Relationship, func
from app.common.utils import generate_uuid4

class Address(SQLModel, table=True):

    __tablename__ = "addresses"

    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True)
    AddressLine1: str = Field(max_length=512)
    AddressLine2: str = Field(default=None, max_length=512)
    City: str = Field(max_length=64)
    State: str = Field(default=None, max_length=64)
    Country: str = Field(default=None, max_length=64)
    ZipCode: str = Field(default=None, max_length=64)
    CreatedBy: str = Field(default=None, max_length=36)
    CreatedAt: datetime = Field(default_factory=func.now(), sa_column_kwargs={"timezone": True})
    UpdatedAt: datetime = Field(default=None, sa_column_kwargs={"onupdate": func.now(), "timezone": True})

    def __repr__(self):
        return json.dumps(self.dict())
