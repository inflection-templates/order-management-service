from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime

class UserLoginSessionCreateModel(BaseModel):
    id        : Optional[UUID4]     = Field(default=None, description="Unique identifier for the user login session")
    UserId    : UUID4               = Field(description="Unique identifier of the user associated with this session")
    IsActive  : bool                = Field(description="Indicates whether the session is currently active")
    StartedAt : Optional[datetime]  = Field(default=None, description="Timestamp when the session started")
    ValidTill : Optional[datetime]  = Field(default=None, description="Timestamp until when the session is valid")

UserLoginSessionCreateModel.model_rebuild()
class UserLoginSessionResponseModel(BaseModel):
    id        : UUID4
    UserId    : UUID4
    IsActive  : bool
    StartedAt : Optional[datetime] = None
    ValidTill : Optional[datetime] = None
    
UserLoginSessionResponseModel.model_rebuild()