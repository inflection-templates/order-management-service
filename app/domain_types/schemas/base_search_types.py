from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class BaseSearchFilter(BaseModel):
    CreatedDateFrom  : Optional[datetime] = Field(default=None, description="Search by created date after this with date format: YYYY-MM-DD")
    CreatedDateTo    : Optional[datetime] = Field(default=None, description="Search by created date before this with date format: YYYY-MM-DD")
    OrderBy          : Optional[str]      = Field(default='CreatedAt', min_length=2, max_length=64, description="Sort by this field")
    OrderByDescending: Optional[bool]     = Field(default=True, description="Sort by descending or ascending")
    PageIndex        : Optional[int]      = Field(default=0, ge=0, le=10000, description="Page index")
    ItemsPerPage     : Optional[int]      = Field(default=10, ge=1, le=100, description="Items per page")

class BaseSearchResults(BaseModel):
    TotalCount       : int  = Field(default=0, ge=0, description="Total count of items")
    RetrievedCount   : int  = Field(default=0, ge=0, description="Retrieved count of items")
    PageIndex        : int  = Field(default=0, ge=0, le=10000, description="Page index")
    ItemsPerPage     : int  = Field(default=10, ge=1, le=100, description="Items per page")
    OrderBy          : str  = Field(default='CreatedAt', min_length=2, max_length=64, description="Sort by this field")
    OrderByDescending: bool = Field(Default=True, description="Sort by descending or ascending")
