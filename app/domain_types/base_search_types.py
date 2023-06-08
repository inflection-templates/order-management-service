from pydantic import BaseModel, Field
from datetime import datetime

class BaseSearchFilter(BaseModel):
    CreatedDateFrom: datetime = Field(Optional=True)
    CreatedDateTo: datetime = Field(Optional=True)
    OrderBy: str = Field(Optional=True)
    OrderByDescending: bool = Field(Optional=True)
    PageIndex: int = Field(Optional=True)
    ItemsPerPage: int = Field(Optional=True)

class BaseSearchResults(BaseModel):
    TotalCount: int = Field(default=0, Optional=False)
    RetrievedCount: int = Field(default=0, Optional=False)
    PageIndex: int = Field(default=0, Optional=False)
    ItemsPerPage: int = Field(default=0, Optional=False)
    OrderBy: str = Field(Optional=True)
    OrderByDescending: bool = Field(Optional=True)
    Items: list = Field(default=None, Optional=True)

