from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class BaseSearchFilter(BaseModel):
    CreatedDateFrom  : Optional[datetime] = Field(default=None)
    CreatedDateTo    : Optional[datetime] = Field(default=None)
    OrderBy          : Optional[str]      = Field(default='CreatedAt', min_length=2, max_length=64)
    OrderByDescending: Optional[bool]     = Field(default=True)
    PageIndex        : Optional[int]      = Field(default=0, ge=0, le=10000)
    ItemsPerPage     : Optional[int]      = Field(default=10, ge=1, le=100)

class BaseSearchResults(BaseModel):
    TotalCount       : int  = Field(default=0, ge=0)
    RetrievedCount   : int  = Field(default=0, ge=0)
    PageIndex        : int  = Field(default=0, ge=0, le=10000)
    ItemsPerPage     : int  = Field(default=10, ge=1, le=100)
    OrderBy          : str  = Field(default='CreatedAt', min_length=2, max_length=64)
    OrderByDescending: bool = Field(Default=True)
