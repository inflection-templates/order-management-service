# Setup using Poetry

This guide shows how to set up the Order Management Service using Poetry for modern Python dependency management.

## Prerequisites

- Python 3.9 or higher
- pip package manager

## What is Poetry?

Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.

## Installation

### 1. Install pipx (Recommended)

**Windows:**
```cmd
pip install --user pipx
pipx ensurepath
```

**Linux/macOS:**
```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Close and reopen your terminal after installation.

### 2. Install Poetry

```bash
pipx install poetry
```

Verify installation:
```bash
poetry --version
```

### 3. Update PATH Variables (Windows)

1. Go to `C:\Users\<Username>\.local\bin`
2. Run `pipx ensurepath`
3. Close and reopen terminal

## Project Setup

### 1. Initialize Poetry Project

**For existing project (our case):**
```bash
cd order-management-service
poetry init
```

Follow the interactive prompts to configure your project.

**For new project:**
```bash
poetry new order-management-service
cd order-management-service
```

### 2. Configure pyproject.toml

The project already has a `pyproject.toml` file. Update it with authentication dependencies:

```toml
[tool.poetry]
name = "order-management-service"
version = "0.1.0"
description = "A generic multi-purpose order management service with authentication"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.9"
fastapi = "^0.104.1"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
sqlalchemy = "^2.0.23"
alembic = "^1.13.1"
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"
PyJWT = {extras = ["crypto"], version = "^2.8.0"}
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
pyotp = "^2.9.0"
qrcode = {extras = ["pil"], version = "^7.4.2"}
email-validator = "^2.1.0"
httpx = "^0.25.2"
python-dotenv = "^1.0.0"
python-multipart = "^0.0.6"
Pillow = "^10.1.0"
PyMySQL = "^1.1.0"
mysql-connector-python = "^8.2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"
httpx = "^0.25.2"
faker = "^20.1.0"
pytest-cov = "^4.1.0"
pytest-asyncio = "^0.21.1"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### 3. Install Dependencies

```bash
# Install all dependencies
poetry install

# Install only production dependencies
poetry install --only main

# Install with development dependencies (default)
poetry install --with dev
```

### 4. Setup Environment Variables

1. Create a `.env` file:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your configuration (see venv-setup.md for details)

### 5. Database Setup

```bash
# Run migrations
poetry run alembic upgrade head
```

### 6. Run the Server

```bash
# Run with poetry
poetry run uvicorn main:app --port 12345 --reload

# Or activate shell and run directly
poetry shell
uvicorn main:app --port 12345 --reload
```

## Poetry Commands Reference

### Environment Management
```bash
# Create virtual environment and install dependencies
poetry install

# Activate virtual environment shell
poetry shell

# Run command in virtual environment
poetry run <command>

# Show virtual environment info
poetry env info

# List virtual environments
poetry env list

# Remove virtual environment
poetry env remove python
```

### Dependency Management
```bash
# Add dependency
poetry add package-name

# Add development dependency
poetry add package-name --group dev

# Add dependency with version constraint
poetry add "package-name>=1.0,<2.0"

# Add dependency with extras
poetry add "package-name[extra1,extra2]"

# Remove dependency
poetry remove package-name

# Update dependencies
poetry update

# Update specific package
poetry update package-name

# Show dependency tree
poetry show --tree

# Show outdated packages
poetry show --outdated
```

### Lock File Management
```bash
# Update poetry.lock
poetry lock

# Install from lock file only
poetry install --only-root

# Export to requirements.txt
poetry export -f requirements.txt --output requirements.txt

# Export dev dependencies too
poetry export -f requirements.txt --output requirements.txt --with dev
```

### Build and Publish
```bash
# Build package
poetry build

# Publish to PyPI
poetry publish

# Check package
poetry check
```

## Development Workflow

### 1. Daily Development
```bash
# Activate environment
poetry shell

# Or run commands with poetry run
poetry run uvicorn main:app --port 12345 --reload

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=app tests/
```

### 2. Adding Dependencies

**Runtime dependency:**
```bash
poetry add requests
```

**Development dependency:**
```bash
poetry add pytest --group dev
```

**Optional dependency:**
```bash
poetry add redis --optional
```

**With version constraints:**
```bash
poetry add "fastapi>=0.100.0,<1.0.0"
```

### 3. Managing Environments

**Create environment with specific Python version:**
```bash
poetry env use python3.9
```

**Show environment location:**
```bash
poetry env info --path
```

**Remove environment:**
```bash
poetry env remove python
```

## Configuration

### poetry.toml (Project Configuration)

Create `poetry.toml` in project root:

```toml
[virtualenvs]
create = true
in-project = true  # Create .venv in project directory
```

### Global Configuration

```bash
# Set global configuration
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true

# View configuration
poetry config --list

# Reset configuration
poetry config virtualenvs.create --unset
```

## Production Deployment

### 1. Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Configure poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main

# Copy application
COPY . .

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Using requirements.txt

```bash
# Export dependencies
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Deploy using pip
pip install -r requirements.txt
```

### 3. Direct Poetry Installation

```bash
# Install only production dependencies
poetry install --only main

# Run production server
poetry run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Troubleshooting

### Common Issues

1. **Poetry not found after installation:**
   ```bash
   # Add to PATH (Linux/macOS)
   export PATH="$HOME/.local/bin:$PATH"

   # Windows: Add C:\Users\<username>\.local\bin to PATH
   ```

2. **Virtual environment issues:**
   ```bash
   poetry env remove python  # Remove environment
   poetry install  # Recreate environment
   ```

3. **Lock file conflicts:**
   ```bash
   poetry lock --no-update  # Lock without updating
   poetry install  # Install from lock
   ```

4. **Dependency resolution issues:**
   ```bash
   poetry add package-name --dry-run  # Test before adding
   poetry update --dry-run  # Test updates
   ```

### Best Practices

1. **Always commit pyproject.toml and poetry.lock**
2. **Use version constraints wisely**
3. **Separate dev and production dependencies**
4. **Use `poetry check` to validate configuration**
5. **Keep poetry updated: `poetry self update`**
6. **Use dependency groups for organization**

## Advantages of Poetry

- **Modern dependency resolution**
- **Automatic virtual environment management**
- **Lockfile for reproducible builds**
- **Built-in build and publish tools**
- **Better dependency constraint handling**
- **Integration with modern Python packaging standards**
- **Excellent CLI interface**

## Migration from requirements.txt

```bash
# Import from requirements.txt
poetry add $(cat requirements.txt | grep -v '^#' | grep -v '^$' | tr '\n' ' ')

# Or use poetry import (if available)
poetry import requirements.txt
```

For more information, visit: https://python-poetry.org/docs/
