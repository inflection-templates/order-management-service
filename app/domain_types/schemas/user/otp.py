
from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime

class OtpCreateModel(BaseModel):
    UserId    : UUID4               = Field(description="Unique identifier of the user")
    Purpose   : str                 = Field(description="Purpose of the OTP, such as login or transaction verification")
    Otp       : str                 = Field(description="The One-Time Password (OTP) value")
    ValidFrom : Optional[datetime]  = Field(default=None, description="Timestamp when the OTP becomes valid")
    ValidTill : Optional[datetime]  = Field(default=None, description="Timestamp when the OTP expires")

OtpCreateModel.model_rebuild()

class OtpResponseModel(BaseModel):
    id        : UUID4
    UserId    : UUID4
    Purpose   : str
    Otp       : str
    ValidFrom : Optional[datetime] = None
    ValidTill : Optional[datetime] = None
    
OtpResponseModel.model_rebuild()
