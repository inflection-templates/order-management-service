# Setup using Python venv

This guide shows how to set up the Order Management Service using Python's built-in virtual environment.

## Prerequisites

- Python 3.9 or higher
- pip package manager

## Setup Steps

### 1. Create Virtual Environment

```bash
python3 -m venv env
```

On Windows:
```cmd
python -m venv env
```

### 2. Activate Virtual Environment

**Linux/macOS:**
```bash
source env/bin/activate
```

**Windows (Command Prompt):**
```cmd
env\Scripts\activate
```

**Windows (PowerShell):**
```powershell
env\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter issues with Rust dependencies, use:
```bash
pip install -r requirements-minimal.txt
```

### 4. Setup Environment Variables

1. Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your configuration:
```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_NAME=order_management
DB_USER_NAME=your_db_user
DB_USER_PASSWORD=your_db_password

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production

# Email Configuration (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=noreply@yourcompany.com

# SMS Configuration (optional)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_phone
```

### 5. Database Setup

1. Install database driver:
```bash
# For MySQL
pip install pymysql

# For PostgreSQL
pip install psycopg2-binary
```

2. Run database migrations:
```bash
alembic upgrade head
```

### 6. Run the Server

```bash
uvicorn main:app --port 12345 --reload
```

The server will be available at `http://localhost:12345`

### 7. Verify Installation

Test the API:
```bash
curl http://localhost:12345/docs
```

## Managing Dependencies

### Add New Package
```bash
pip install package-name
pip freeze > requirements.txt
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

### Deactivate Virtual Environment
```bash
deactivate
```

## Troubleshooting

### Common Issues

1. **Permission Errors on Windows:**
   - Run PowerShell as Administrator
   - Enable script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

2. **Package Installation Fails:**
   - Update pip: `pip install --upgrade pip`
   - Use requirements-minimal.txt for systems without Rust compiler

3. **Database Connection Issues:**
   - Verify database is running
   - Check connection string in .env file
   - Ensure database user has proper permissions

### Development Mode

For development with auto-reload:
```bash
uvicorn main:app --port 12345 --reload --log-level debug
```

### Testing

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app tests/
```
