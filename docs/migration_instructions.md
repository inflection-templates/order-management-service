# Database Migration Instructions

## Overview
The authentication system requires several new database tables and modifications to existing tables.

## Required Dependencies

First, install the required Python packages:

```bash
pip install python-jose[cryptography] pyotp qrcode[pil] httpx email-validator
```

Or update your requirements.txt and run:
```bash
pip install -r requirements.txt
```

## Database Changes

### New Tables

1. **tenants** - Multi-tenant support
2. **auth_tokens** - JWT token management
3. **user_external_auths** - External authentication providers
4. **otps** - OTP management (replaces existing otp table)

### Modified Tables

1. **users** - Added authentication and tenant fields

## Migration Steps

### 1. Create Migration

```bash
alembic revision --autogenerate -m "Add authentication system tables"
```

### 2. Review Migration

Check the generated migration file in `alembic/versions/` and ensure it includes:

- Create `tenants` table
- Create `auth_tokens` table
- Create `user_external_auths` table
- Update `otps` table structure
- Add new columns to `users` table:
  - `TenantId` (foreign key to tenants)
  - `IsActive` (boolean)
  - `IsEmailVerified` (boolean)
  - `IsPhoneVerified` (boolean)
  - `IsTwoFactorEnabled` (boolean)
  - `TwoFactorSecret` (string)
  - `LastLoginAt` (datetime)
  - `FailedLoginAttempts` (integer)
  - `LockedUntil` (datetime)
  - `ExternalProviders` (text/json)

### 3. Run Migration

```bash
alembic upgrade head
```

### 4. Create Default Tenant

After migration, create the default tenant:

```sql
INSERT INTO tenants (id, Name, Code, IsDefault, IsActive)
VALUES ('default', 'Default Tenant', 'default', 1, 1);
```

### 5. Update Existing Users

Associate existing users with the default tenant:

```sql
UPDATE users SET TenantId = 'default' WHERE TenantId IS NULL;
```

## Post-Migration Setup

### 1. Environment Configuration

Update your `.env` file with authentication settings (see authentication.md for full configuration).

### 2. Test Authentication

Test the authentication endpoints:

```bash
# Test login
curl -X POST http://localhost:12345/api/v1/auth/login/email \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Test profile (with token from login)
curl -X GET http://localhost:12345/api/v1/auth/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Update Client Applications

Update your client applications to:
- Use the new authentication endpoints
- Include JWT tokens in API requests
- Handle token refresh
- Support multi-tenant headers if needed

## Rollback Instructions

If you need to rollback the migration:

```bash
alembic downgrade -1
```

**Warning**: This will remove all authentication tables and data. Make sure to backup your database first.

## Troubleshooting

### Common Issues

1. **Foreign Key Constraints**: Ensure all existing users have valid tenant associations
2. **Column Defaults**: Some new columns may need default values for existing records
3. **Index Creation**: Large user tables may take time to add new indexes

### Verification Queries

Check that migration completed successfully:

```sql
-- Verify new tables exist
SHOW TABLES LIKE 'tenants';
SHOW TABLES LIKE 'auth_tokens';
SHOW TABLES LIKE 'user_external_auths';

-- Verify user table updates
DESCRIBE users;

-- Check default tenant exists
SELECT * FROM tenants WHERE Code = 'default';

-- Verify users are associated with tenant
SELECT COUNT(*) FROM users WHERE TenantId IS NOT NULL;
```

## Data Migration Scripts

If you have existing user data that needs special handling, create custom migration scripts:

```python
# Example: Migrate existing user sessions
from sqlalchemy.orm import Session
from app.database.models.user import User
from app.database.models.tenant import Tenant

def migrate_existing_users(session: Session):
    # Get default tenant
    default_tenant = session.query(Tenant).filter(Tenant.Code == 'default').first()

    # Update users without tenant
    users_without_tenant = session.query(User).filter(User.TenantId.is_(None)).all()

    for user in users_without_tenant:
        user.TenantId = default_tenant.id
        user.IsActive = True
        user.IsEmailVerified = True  # Assume existing users are verified

    session.commit()
```

Run such scripts after the main migration but before starting the application.
