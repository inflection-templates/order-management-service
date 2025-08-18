# Installation Guide

## Requirements Installation (No Rust Dependencies)

The authentication system has been updated to avoid Rust dependencies that can cause installation issues on Windows and other systems.

### Option 1: Standard Installation

```bash
pip install -r requirements.txt
```

### Option 2: Minimal Installation (if you encounter issues)

```bash
pip install -r requirements-minimal.txt
```

### Option 3: Manual Installation (step by step)

If you're still having issues, install packages individually:

```bash
# Core web framework
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install starlette==0.27.0

# Pydantic
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0

# Database
pip install SQLAlchemy==2.0.23
pip install alembic==1.13.1
pip install PyMySQL==1.1.0

# Authentication (using PyJWT instead of python-jose to avoid Rust)
pip install "PyJWT[crypto]==2.8.0"
pip install "passlib[bcrypt]==1.7.4"
pip install pyotp==2.9.0
pip install "qrcode[pil]==7.4.2"
pip install email-validator==2.1.0
pip install cryptography==41.0.8

# HTTP Client
pip install httpx==0.25.2
pip install requests==2.31.0

# Utilities
pip install python-dotenv==1.0.0
pip install python-multipart==0.0.6
pip install Pillow==10.1.0
```

## Packages Removed to Avoid Rust Dependencies

The following packages were removed or replaced to avoid Rust compilation issues:

- ❌ `rpds-py` - Requires Rust compiler
- ❌ `orjson` - Requires Rust compiler (using standard JSON instead)
- ❌ `watchfiles` - Requires Rust compiler (using uvicorn's built-in reloader)
- ❌ `python-jose` - Replaced with `PyJWT` (no Rust dependency)

## JWT Library Change

**Important**: The authentication system now uses `PyJWT` instead of `python-jose` to avoid Rust dependencies. The JWT service automatically detects which library is available:

1. **Primary**: Uses `PyJWT` (recommended, no Rust)
2. **Fallback**: Uses `python-jose` if PyJWT is not available

## Verification

After installation, verify the authentication system works:

```python
# Test JWT functionality
from app.auth.jwt_service import JWTService

# This should work without errors
token = JWTService.create_access_token("test_user", "default", ["user"])
print("JWT creation successful!")
```

## Troubleshooting

### Issue: Rust Compiler Required

**Error**: `error: Microsoft Visual C++ 14.0 is required` or `Rust compiler not found`

**Solution**: Use the updated requirements.txt which avoids Rust dependencies entirely.

### Issue: Cryptography Installation Fails

**Error**: `Failed building wheel for cryptography`

**Solutions**:
1. Update pip: `pip install --upgrade pip`
2. Install pre-compiled wheel: `pip install --only-binary=all cryptography==41.0.8`
3. On Windows, install Visual C++ Build Tools

### Issue: PyJWT vs python-jose

The system automatically handles both libraries. If you have both installed, PyJWT takes precedence (which is preferred for avoiding Rust dependencies).

### Issue: Pillow Installation

If Pillow fails to install:
```bash
# On Ubuntu/Debian
sudo apt-get install libjpeg-dev zlib1g-dev

# On CentOS/RHEL
sudo yum install libjpeg-devel zlib-devel

# On macOS
brew install libjpeg

# Then install Pillow
pip install Pillow==10.1.0
```

## Development vs Production

### Development
```bash
pip install -r requirements.txt
# or
pip install -r requirements-minimal.txt
```

### Production
For production, consider using:
- Docker (recommended)
- Virtual environment with pinned versions
- Additional security packages

```bash
# Additional production packages (optional)
pip install gunicorn==21.2.0  # Production WSGI server
pip install redis==5.0.1      # For session storage/caching
```

## Docker Alternative

If you continue to have installation issues, use Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Next Steps

After successful installation:

1. **Configure Environment**: Update your `.env` file with JWT secrets
2. **Run Migration**: `alembic upgrade head`
3. **Test Authentication**: Use the provided API endpoints
4. **Start Application**: `uvicorn main:app --reload`

## Support

If you continue to have installation issues:

1. Check Python version (3.9+ recommended)
2. Update pip: `pip install --upgrade pip`
3. Clear pip cache: `pip cache purge`
4. Use virtual environment
5. Try requirements-minimal.txt for basic functionality
