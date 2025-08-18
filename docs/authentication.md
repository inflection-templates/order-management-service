# Authentication System Documentation

## Overview

This order management service now includes a comprehensive multi-tenant authentication system with support for multiple authentication methods, external providers, and user management flows.

## Features

### 🔐 Authentication Methods
- **Email & Password**: Traditional username/password authentication
- **Phone & OTP**: SMS-based one-time password authentication
- **Phone & Password**: Phone number with password authentication
- **Two-Factor Authentication**: TOTP-based 2FA with QR code setup
- **External Providers**: Google, GitHub, Facebook, Twitter, GitLab
- **Enterprise**: AWS Cognito, Azure Active Directory, SAML

### 🏢 Multi-Tenant Architecture
- Each user belongs to a tenant
- System users belong to the default tenant
- Tenant isolation for user data
- Configurable tenant identification (header or subdomain)

### 🎫 JWT Token Management
- Access tokens for API authentication
- Refresh tokens for token renewal
- Special tokens for password reset, email verification, invitations
- Token revocation and blacklisting

### 👥 User Management Flows
- User invitations with email links
- Onboarding welcome emails
- Password reset via email/SMS
- Email and phone verification
- Account lockout after failed attempts

## Quick Start

### 1. Installation

Install the required packages (no Rust dependencies):

```bash
pip install -r requirements.txt
# or for minimal installation:
pip install -r requirements-minimal.txt
```

**Note**: The system now uses `PyJWT` instead of `python-jose` to avoid Rust compilation issues.

### 2. Configuration

Update your `.env` file with authentication settings:

```env
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Multi-tenant
DEFAULT_TENANT_ID=default
TENANT_HEADER_NAME=X-Tenant-ID

# Feature Flags
ENABLE_EMAIL_PASSWORD_AUTH=true
ENABLE_PHONE_OTP_AUTH=true
ENABLE_TWO_FACTOR_AUTH=true
ENABLE_SOCIAL_LOGIN=true

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# SMS Configuration (optional)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-phone
```

### 3. Database Migration

Run the database migration to create the new authentication tables:

```bash
alembic revision --autogenerate -m "Add authentication tables"
alembic upgrade head
```

### 4. Using the Authentication Decorator

Protect your API endpoints using the `@authenticate_user` decorator:

```python
from app.auth import authenticate_user, AuthContext
from fastapi import Request

# Require authentication
@router.get("/protected")
@authenticate_user(required=True)
async def protected_endpoint(
    request: Request,
    auth_context: AuthContext = None
):
    user = auth_context.user
    tenant = auth_context.tenant
    return {"message": f"Hello {user.FirstName}!"}

# Require specific roles
@router.delete("/admin-only")
@authenticate_user(required=True, roles=["admin"])
async def admin_only_endpoint(
    request: Request,
    auth_context: AuthContext = None
):
    return {"message": "Admin access granted"}

# Optional authentication (public endpoint)
@router.get("/public")
@authenticate_user(required=False)
async def public_endpoint(
    request: Request,
    auth_context: AuthContext = None
):
    if auth_context:
        return {"message": f"Hello {auth_context.user.FirstName}!"}
    else:
        return {"message": "Hello anonymous user!"}
```

## API Endpoints

### Authentication Endpoints

#### Login
```http
POST /api/v1/auth/login/email
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123",
    "tenant_id": "optional-tenant-id"
}
```

```http
POST /api/v1/auth/login/phone
Content-Type: application/json

{
    "phone": "+1234567890",
    "password": "password123"
}
```

```http
POST /api/v1/auth/login/phone-otp
Content-Type: application/json

{
    "phone": "+1234567890",
    "otp_code": "123456"
}
```

#### OTP Management
```http
POST /api/v1/auth/otp/send
Content-Type: application/json

{
    "phone": "+1234567890",
    "purpose": "login"
}
```

#### Token Management
```http
POST /api/v1/auth/token/refresh
Content-Type: application/json

{
    "refresh_token": "your-refresh-token"
}
```

```http
POST /api/v1/auth/logout
Authorization: Bearer your-access-token
```

#### User Profile
```http
GET /api/v1/auth/profile
Authorization: Bearer your-access-token
```

#### Two-Factor Authentication
```http
POST /api/v1/auth/2fa/setup
Authorization: Bearer your-access-token
```

```http
POST /api/v1/auth/2fa/verify
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "totp_code": "123456"
}
```

### User Flow Endpoints

#### Password Management
```http
POST /api/v1/auth/password/reset-request
Content-Type: application/json

{
    "email": "user@example.com"
}
```

```http
POST /api/v1/auth/password/reset
Content-Type: application/json

{
    "token": "reset-token",
    "new_password": "newpassword123"
}
```

```http
POST /api/v1/auth/password/change
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "current_password": "oldpassword",
    "new_password": "newpassword123"
}
```

#### User Invitations
```http
POST /api/v1/auth/invite
Authorization: Bearer admin-token
Content-Type: application/json

{
    "email": "newuser@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role_ids": [1, 2]
}
```

```http
POST /api/v1/auth/accept-invitation
Content-Type: application/json

{
    "token": "invitation-token",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Verification
```http
POST /api/v1/auth/verify/email
Content-Type: application/json

{
    "token": "verification-token"
}
```

```http
POST /api/v1/auth/verify/phone/send
Authorization: Bearer your-access-token
```

```http
POST /api/v1/auth/verify/phone
Authorization: Bearer your-access-token
Content-Type: application/json

{
    "otp_code": "123456"
}
```

### External Authentication

#### Get Available Providers
```http
GET /api/v1/auth/providers
```

#### Get Authorization URL
```http
POST /api/v1/auth/external/url
Content-Type: application/json

{
    "provider": "google",
    "redirect_uri": "http://localhost:3000/callback"
}
```

#### Handle Callback
```http
POST /api/v1/auth/external/callback
Content-Type: application/json

{
    "provider": "google",
    "code": "authorization-code",
    "state": "csrf-state"
}
```

## Multi-Tenant Usage

### Header-Based Tenancy
Include the tenant ID in request headers:

```http
GET /api/v1/auth/profile
Authorization: Bearer your-access-token
X-Tenant-ID: your-tenant-id
```

### Subdomain-Based Tenancy
Access different tenants via subdomains:

```
https://tenant1.yourapp.com/api/v1/auth/profile
https://tenant2.yourapp.com/api/v1/auth/profile
```

## Security Features

### Token Security
- JWT tokens with configurable expiration
- Refresh token rotation
- Token revocation and blacklisting
- Secure token storage recommendations

### Account Protection
- Account lockout after failed login attempts
- Rate limiting on sensitive endpoints
- CSRF protection for OAuth flows
- Secure password hashing with bcrypt

### Multi-Factor Authentication
- TOTP-based 2FA with QR code setup
- SMS-based OTP verification
- Backup codes (can be implemented)

## Customization

### Adding New Authentication Providers

1. Create a new provider class extending `BaseAuthProvider`:

```python
from app.auth.providers.base_provider import BaseAuthProvider, ExternalUserInfo

class CustomAuthProvider(BaseAuthProvider):
    @property
    def provider_name(self) -> str:
        return "custom"

    def get_authorization_url(self, state: str = None) -> str:
        # Implementation
        pass

    async def exchange_code_for_token(self, code: str, state: str = None):
        # Implementation
        pass

    async def get_user_info(self, access_token: str) -> ExternalUserInfo:
        # Implementation
        pass
```

2. Register the provider:

```python
from app.auth.providers.provider_factory import ProviderFactory

ProviderFactory.register_provider("custom", CustomAuthProvider)
```

### Custom Authentication Logic

Override methods in `AuthService` to customize authentication behavior:

```python
from app.auth.auth_service import AuthService

class CustomAuthService(AuthService):
    @staticmethod
    def authenticate_with_email_password(session, email, password, tenant_id=None):
        # Custom authentication logic
        pass
```

## Best Practices

### Security
- Use strong JWT secrets in production
- Enable HTTPS for all authentication endpoints
- Implement proper CORS policies
- Store sensitive configuration in environment variables
- Regularly rotate JWT secrets

### Performance
- Use Redis for token blacklisting in production
- Implement caching for user roles and permissions
- Use connection pooling for external API calls
- Monitor authentication endpoint performance

### User Experience
- Provide clear error messages
- Implement progressive enhancement for 2FA
- Use proper loading states during authentication
- Provide fallback authentication methods

## Troubleshooting

### Common Issues

1. **Token Expired**: Implement automatic token refresh on the client side
2. **Invalid Tenant**: Ensure tenant ID is correctly passed in headers or subdomain
3. **2FA Setup Issues**: Verify system time synchronization
4. **OAuth Callback Errors**: Check redirect URI configuration
5. **Database Connection**: Ensure proper database migrations are applied

### Debugging

Enable debug logging for authentication:

```python
import logging
logging.getLogger("app.auth").setLevel(logging.DEBUG)
```

Check authentication status:
```bash
curl -H "Authorization: Bearer your-token" http://localhost:12345/api/v1/auth/profile
```

## Migration Guide

### From Basic Authentication

1. Update existing user records to include tenant association
2. Migrate existing sessions to new JWT format
3. Update client applications to use new authentication endpoints
4. Test all authentication flows thoroughly

### Database Schema Changes

The authentication system adds these new tables:
- `tenants`: Multi-tenant support
- `auth_tokens`: Token management
- `user_external_auths`: External provider linkage
- `otps`: OTP management

Updated tables:
- `users`: Added authentication and tenant fields
- `user_login_sessions`: Enhanced session tracking

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the API documentation
- Check application logs for detailed error messages
- Ensure all dependencies are properly installed
