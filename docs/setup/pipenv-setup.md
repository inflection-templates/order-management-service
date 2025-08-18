# Setup using Pipenv

This guide shows how to set up the Order Management Service using Pipenv for dependency management.

## Prerequisites

- Python 3.9 or higher
- pip package manager

## What is Pipenv?

Pipenv automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your Pipfile as you install/uninstall packages. It also generates the ever-important Pipfile.lock, which is used to produce deterministic builds.

## Setup Steps

### 1. Install Pipenv

```bash
pip3 install pipenv
```

On Windows:
```cmd
pip install pipenv
```

### 2. Create Pipenv Environment

Navigate to your project directory and run:
```bash
pipenv shell
```

This will create a virtual environment in your system's default location:
- **Windows:** `C:\Users\<username>\.virtualenvs\order-management-service-<hash>`
- **Linux/macOS:** `~/.local/share/virtualenvs/order-management-service-<hash>`

### 3. Install Dependencies

**Option A: From requirements.txt**
```bash
pipenv install -r requirements.txt
```

**Option B: Install packages individually**
```bash
# Core dependencies
pipenv install fastapi
pipenv install uvicorn[standard]
pipenv install sqlalchemy
pipenv install alembic
pipenv install pydantic
pipenv install pydantic-settings

# Authentication
pipenv install "PyJWT[crypto]"
pipenv install "passlib[bcrypt]"
pipenv install pyotp
pipenv install "qrcode[pil]"

# Database
pipenv install pymysql
pipenv install mysql-connector-python

# Development dependencies
pipenv install pytest --dev
pipenv install httpx --dev
pipenv install faker --dev
```

### 4. Setup Environment Variables

1. Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your configuration (see venv-setup.md for details)

### 5. Database Setup

```bash
# Run migrations
pipenv run alembic upgrade head
```

### 6. Run the Server

```bash
pipenv run uvicorn main:app --port 12345 --reload
```

Or activate the shell first:
```bash
pipenv shell
uvicorn main:app --port 12345 --reload
```

## Pipenv Commands Reference

### Environment Management
```bash
# Create/activate shell
pipenv shell

# Install from Pipfile
pipenv install

# Install from Pipfile.lock (production)
pipenv install --ignore-pipfile

# Install development dependencies
pipenv install --dev

# Exit shell
exit
```

### Package Management
```bash
# Install package
pipenv install package-name

# Install development package
pipenv install package-name --dev

# Uninstall package
pipenv uninstall package-name

# Update all packages
pipenv update

# Show dependency graph
pipenv graph
```

### Lock File Management
```bash
# Generate Pipfile.lock
pipenv lock

# Install from lock file only
pipenv install --ignore-pipfile

# Check for security vulnerabilities
pipenv check
```

### Environment Information
```bash
# Show virtual environment location
pipenv --venv

# Show project location
pipenv --where

# List installed packages
pipenv run pip list
```

## Development Workflow

### 1. Daily Development
```bash
# Activate environment
pipenv shell

# Start development server
uvicorn main:app --port 12345 --reload

# In another terminal (with pipenv shell active)
pytest  # Run tests
```

### 2. Adding New Dependencies
```bash
# Add runtime dependency
pipenv install new-package

# Add development dependency
pipenv install pytest-cov --dev

# Lock dependencies
pipenv lock
```

### 3. Production Deployment
```bash
# Install only production dependencies
pipenv install --ignore-pipfile --deploy

# Run production server
pipenv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Pipfile Example

After setup, your `Pipfile` should look like this:

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
fastapi = "*"
uvicorn = {extras = ["standard"], version = "*"}
sqlalchemy = "*"
alembic = "*"
pydantic = "*"
pydantic-settings = "*"
pyjwt = {extras = ["crypto"], version = "*"}
passlib = {extras = ["bcrypt"], version = "*"}
pyotp = "*"
qrcode = {extras = ["pil"], version = "*"}
pymysql = "*"
mysql-connector-python = "*"

[dev-packages]
pytest = "*"
httpx = "*"
faker = "*"

[requires]
python_version = "3.9"
```

## Troubleshooting

### Common Issues

1. **Virtual Environment Not Found:**
   ```bash
   pipenv --rm  # Remove current environment
   pipenv install  # Recreate environment
   ```

2. **Lock File Issues:**
   ```bash
   pipenv lock --clear  # Clear cache and regenerate lock
   ```

3. **Package Installation Fails:**
   ```bash
   pipenv install --skip-lock  # Skip lock file generation
   pipenv lock  # Generate lock file separately
   ```

4. **Python Version Issues:**
   ```bash
   pipenv --python 3.9  # Specify Python version
   ```

### Best Practices

1. **Always commit both Pipfile and Pipfile.lock**
2. **Use `pipenv lock` after adding dependencies**
3. **Use `--dev` flag for development-only packages**
4. **Run `pipenv check` regularly for security issues**
5. **Use `pipenv install --ignore-pipfile` in production**

## Advantages of Pipenv

- **Automatic virtualenv management**
- **Dependency resolution and locking**
- **Security vulnerability scanning**
- **Deterministic builds with Pipfile.lock**
- **Development vs production dependencies separation**
- **Integration with .env files**

For more information, visit: https://pipenv.pypa.io/en/latest/
