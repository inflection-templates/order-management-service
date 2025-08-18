# Order Management Service - Setup Guide

This directory contains comprehensive setup guides for different development environments and deployment methods.

## 🚀 Quick Start

Choose your preferred setup method:

| Method | Best For | Time | Difficulty |
|--------|----------|------|------------|
| [Docker](docker-setup.md) | Quick start, consistent environment | 5 min | ⭐ Easy |
| [venv](venv-setup.md) | Simple Python development | 10 min | ⭐⭐ Medium |
| [Pipenv](pipenv-setup.md) | Modern dependency management | 15 min | ⭐⭐ Medium |
| [Poetry](poetry-setup.md) | Advanced Python project management | 20 min | ⭐⭐⭐ Advanced |
| [VS Code](vscode-setup.md) | Full IDE development experience | 30 min | ⭐⭐⭐ Advanced |

## 📋 Prerequisites

### System Requirements
- **Python**: 3.9 or higher
- **Database**: MySQL 8.0+ or PostgreSQL 12+
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space

### Optional Requirements
- **Docker**: For containerized deployment
- **Redis**: For session storage and caching (production)
- **SMTP Server**: For email functionality
- **Twilio Account**: For SMS functionality

## 🎯 Recommended Setup Path

### For Beginners
1. **[Docker Setup](docker-setup.md)** - Fastest way to get started
2. **[VS Code Setup](vscode-setup.md)** - Best development experience

### For Python Developers
1. **[venv Setup](venv-setup.md)** - Simple and familiar
2. **[VS Code Setup](vscode-setup.md)** - Enhanced development tools

### For Advanced Users
1. **[Poetry Setup](poetry-setup.md)** - Modern dependency management
2. **[VS Code Setup](vscode-setup.md)** - Full IDE experience

### For Teams
1. **[Docker Setup](docker-setup.md)** - Consistent environments
2. **[Pipenv Setup](pipenv-setup.md)** - Collaborative dependency management

## 🔧 Setup Comparison

| Feature | venv | Pipenv | Poetry | Docker |
|---------|------|--------|--------|--------|
| **Simplicity** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Dependency Management** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Reproducibility** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Team Collaboration** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Production Ready** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Learning Curve** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

## 📚 Setup Guides

### [🐍 venv Setup](venv-setup.md)
Traditional Python virtual environment setup using the built-in `venv` module.

**Pros:**
- Built into Python
- Simple and straightforward
- Widely supported
- No additional tools required

**Cons:**
- Manual dependency management
- No automatic lock files
- Basic environment isolation

### [📦 Pipenv Setup](pipenv-setup.md)
Modern Python dependency management with automatic virtual environment handling.

**Pros:**
- Automatic virtual environment management
- Pipfile and Pipfile.lock for reproducible builds
- Built-in security vulnerability scanning
- Excellent for development workflows

**Cons:**
- Additional tool to learn
- Can be slower than alternatives
- Sometimes complex dependency resolution

### [🎭 Poetry Setup](poetry-setup.md)
Advanced Python project management with modern packaging standards.

**Pros:**
- Modern dependency resolution
- Built-in build and publish tools
- Excellent lockfile management
- Great for library development
- PEP 518 compliant

**Cons:**
- Steeper learning curve
- Additional configuration
- May be overkill for simple projects

### [🐳 Docker Setup](docker-setup.md)
Containerized development and deployment with consistent environments.

**Pros:**
- Consistent environments across systems
- Includes all dependencies
- Production-ready deployment
- Easy scaling and orchestration
- Database included

**Cons:**
- Requires Docker knowledge
- Resource overhead
- Debugging can be more complex

### [💻 VS Code Setup](vscode-setup.md)
Comprehensive IDE setup with debugging, testing, and development tools.

**Pros:**
- Full debugging capabilities
- Integrated testing
- Code formatting and linting
- API testing tools
- Database management

**Cons:**
- IDE-specific setup
- More complex configuration
- Requires VS Code

## 🔄 Migration Between Setups

### From venv to Poetry
```bash
# Export current requirements
pip freeze > requirements.txt

# Initialize Poetry project
poetry init

# Import requirements
cat requirements.txt | grep -E '^[^# ]' | cut -d= -f1 | xargs -n 1 poetry add
```

### From requirements.txt to Pipenv
```bash
# Install from requirements.txt
pipenv install -r requirements.txt

# Generate Pipfile.lock
pipenv lock
```

### To Docker from any setup
```bash
# Copy your current requirements.txt to project root
# Follow Docker setup guide
docker-compose up --build
```

## 🚀 After Setup

Once you've completed your chosen setup, you'll need to:

### 1. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your settings
```

### 2. Setup Database
```bash
# Run migrations
alembic upgrade head
```

### 3. Verify Installation
```bash
# Test the API
curl http://localhost:12345/docs
```

### 4. Run Tests
```bash
pytest tests/
```

## 🔍 Troubleshooting

### Common Issues

1. **Python Version Issues**
   - Ensure Python 3.9+ is installed
   - Use `python --version` to check

2. **Database Connection**
   - Verify database is running
   - Check connection string in `.env`

3. **Port Already in Use**
   - Change port in configuration
   - Kill existing processes

4. **Package Installation Fails**
   - Update pip: `pip install --upgrade pip`
   - Try requirements-minimal.txt for Rust issues

5. **Authentication Not Working**
   - Check JWT_SECRET_KEY in .env
   - Verify database migrations ran

### Getting Help

- **Documentation**: Check individual setup guides
- **Issues**: Create GitHub issue with setup method and error
- **Logs**: Include relevant error messages and logs

## 🎯 Next Steps

After successful setup:

1. **[Authentication Guide](../authentication.md)** - Learn about the auth system
2. **[API Documentation](../api/)** - Explore available endpoints
3. **[Development Guide](../development.md)** - Development best practices
4. **[Testing Guide](../testing.md)** - How to write and run tests
5. **[Deployment Guide](../deployment.md)** - Production deployment

## 📝 Contributing

When adding new setup methods:

1. Create a new markdown file in `docs/setup/`
2. Follow the existing structure and format
3. Include troubleshooting section
4. Update this README with the new method
5. Test the setup on a clean system

---

**Need help?** Choose the setup method that matches your experience level and requirements. The Docker setup is recommended for the quickest start, while Poetry is best for advanced Python development.
