from pydantic import BaseModel, Field
try:
    from pydantic import EmailStr
except ImportError:
    from email_validator import EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

# Login Models
class EmailPasswordLoginModel(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")
    tenant_id: Optional[str] = Field(None, description="Tenant ID (optional)")

class PhonePasswordLoginModel(BaseModel):
    phone: str = Field(..., description="User phone number")
    password: str = Field(..., min_length=6, description="User password")
    tenant_id: Optional[str] = Field(None, description="Tenant ID (optional)")

class PhoneOTPLoginModel(BaseModel):
    phone: str = Field(..., description="User phone number")
    otp_code: str = Field(..., min_length=4, max_length=8, description="OTP code")
    tenant_id: Optional[str] = Field(None, description="Tenant ID (optional)")

class SendOTPModel(BaseModel):
    phone: Optional[str] = Field(None, description="Phone number for SMS OTP")
    email: Optional[EmailStr] = Field(None, description="Email for email OTP")
    purpose: str = Field(..., description="OTP purpose (login, phone_verification, email_verification, password_reset)")

class TwoFactorLoginModel(BaseModel):
    access_token: str = Field(..., description="Temporary access token from first factor")
    totp_code: str = Field(..., min_length=6, max_length=6, description="TOTP code from authenticator app")

# Registration Models
class UserRegistrationModel(BaseModel):
    first_name: Optional[str] = Field(None, max_length=70)
    last_name: Optional[str] = Field(None, max_length=70)
    email: Optional[EmailStr] = Field(None, description="User email address")
    phone: Optional[str] = Field(None, description="User phone number")
    password: str = Field(..., min_length=6, description="User password")
    tenant_id: Optional[str] = Field(None, description="Tenant ID (optional)")
    country_code: Optional[str] = Field("+1", description="Country code for phone")

# Token Models
class TokenResponseModel(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: Optional[int] = Field(None, description="Token expiration in seconds")
    requires_2fa: Optional[bool] = Field(False, description="Whether 2FA is required")

class RefreshTokenModel(BaseModel):
    refresh_token: str = Field(..., description="Refresh token")

# Password Reset Models
class PasswordResetRequestModel(BaseModel):
    email: Optional[EmailStr] = Field(None, description="User email address")
    phone: Optional[str] = Field(None, description="User phone number")
    tenant_id: Optional[str] = Field(None, description="Tenant ID (optional)")

class PasswordResetModel(BaseModel):
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=6, description="New password")

class ChangePasswordModel(BaseModel):
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=6, description="New password")

# Two-Factor Authentication Models
class TwoFactorSetupResponseModel(BaseModel):
    secret: str = Field(..., description="TOTP secret key")
    qr_code: str = Field(..., description="QR code data URL")
    provisioning_uri: str = Field(..., description="TOTP provisioning URI")

class TwoFactorVerificationModel(BaseModel):
    totp_code: str = Field(..., min_length=6, max_length=6, description="TOTP code")

# External Authentication Models
class ExternalAuthCallbackModel(BaseModel):
    provider: str = Field(..., description="Authentication provider")
    code: str = Field(..., description="Authorization code")
    state: Optional[str] = Field(None, description="State parameter")
    tenant_id: Optional[str] = Field(None, description="Tenant ID")

class ExternalAuthURLModel(BaseModel):
    provider: str = Field(..., description="Authentication provider")
    redirect_uri: str = Field(..., description="Redirect URI after authentication")
    tenant_id: Optional[str] = Field(None, description="Tenant ID")

# User Profile Models
class UserProfileModel(BaseModel):
    id: str
    tenant_id: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    is_email_verified: bool
    is_phone_verified: bool
    is_two_factor_enabled: bool
    last_login_at: Optional[datetime]
    created_at: datetime

# Invitation Models
class UserInvitationModel(BaseModel):
    email: EmailStr = Field(..., description="Email address to invite")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    role_ids: Optional[list[int]] = Field(None, description="Role IDs to assign")
    tenant_id: Optional[str] = Field(None, description="Tenant ID")
    message: Optional[str] = Field(None, description="Custom invitation message")

class AcceptInvitationModel(BaseModel):
    token: str = Field(..., description="Invitation token")
    password: str = Field(..., min_length=6, description="User password")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")

# Verification Models
class EmailVerificationModel(BaseModel):
    token: str = Field(..., description="Email verification token")

class PhoneVerificationModel(BaseModel):
    otp_code: str = Field(..., min_length=4, max_length=8, description="OTP code")

# Session Models
class UserSessionModel(BaseModel):
    id: str
    user_id: str
    is_active: bool
    created_at: datetime
    expires_at: datetime
    last_activity: Optional[datetime]
    ip_address: Optional[str]
    user_agent: Optional[str]

# Auth Context Models
class AuthContextModel(BaseModel):
    user: UserProfileModel
    tenant_id: str
    roles: list[str]
    permissions: Optional[list[str]] = None
