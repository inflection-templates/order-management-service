# VS Code Development Setup

This guide shows how to set up Visual Studio Code for optimal development experience with the Order Management Service.

## Prerequisites

- Visual Studio Code
- Python 3.9 or higher
- Git

## VS Code Extensions

### Essential Extensions

Install these extensions for the best development experience:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-python.flake8",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml",
    "ms-vscode.vscode-docker",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.rest-client",
    "humao.rest-client",
    "ms-vscode.vscode-thunder-client"
  ]
}
```

### Python Development Extensions
- **Python** - Python language support
- **Pylance** - Fast, feature-rich Python language server
- **Black Formatter** - Python code formatter
- **isort** - Import statement organizer
- **Flake8** - Python linting

### Additional Useful Extensions
- **Docker** - Docker container management
- **REST Client** - Test API endpoints directly in VS Code
- **Thunder Client** - Lightweight REST API client
- **GitLens** - Enhanced Git capabilities
- **Todo Tree** - TODO comment highlighting
- **Bracket Pair Colorizer** - Colorize matching brackets

## Project Configuration

### 1. Workspace Settings

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "./env/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.pylintEnabled": false,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "python.testing.unittestEnabled": false,
  "python.testing.autoTestDiscoverOnSaveEnabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".pytest_cache": true,
    ".coverage": true,
    "htmlcov": true
  },
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoImportCompletions": true
}
```

### 2. Launch Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch Server",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "args": [],
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      },
      "envFile": "${workspaceFolder}/.env",
      "cwd": "${workspaceFolder}",
      "autoReload": {
        "enable": true
      }
    },
    {
      "name": "Launch Server (Debug Mode)",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "12345",
        "--reload",
        "--log-level",
        "debug"
      ],
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      },
      "envFile": "${workspaceFolder}/.env",
      "cwd": "${workspaceFolder}"
    },
    {
      "name": "Run Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "tests/",
        "-v",
        "--tb=short"
      ],
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      },
      "envFile": "${workspaceFolder}/.env.test",
      "cwd": "${workspaceFolder}"
    },
    {
      "name": "Run Tests with Coverage",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "tests/",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=term"
      ],
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      },
      "envFile": "${workspaceFolder}/.env.test",
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### 3. Tasks Configuration

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Development Server",
      "type": "shell",
      "command": "uvicorn",
      "args": [
        "main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "12345",
        "--reload"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "new"
      },
      "problemMatcher": []
    },
    {
      "label": "Run Tests",
      "type": "shell",
      "command": "pytest",
      "args": [
        "tests/",
        "-v"
      ],
      "group": "test",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "new"
      }
    },
    {
      "label": "Format Code",
      "type": "shell",
      "command": "black",
      "args": [
        "app/",
        "tests/"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "silent",
        "focus": false,
        "panel": "shared"
      }
    },
    {
      "label": "Lint Code",
      "type": "shell",
      "command": "flake8",
      "args": [
        "app/",
        "tests/"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      }
    },
    {
      "label": "Database Migration",
      "type": "shell",
      "command": "alembic",
      "args": [
        "upgrade",
        "head"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      }
    },
    {
      "label": "Create Migration",
      "type": "shell",
      "command": "alembic",
      "args": [
        "revision",
        "--autogenerate",
        "-m",
        "${input:migrationMessage}"
      ],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      }
    }
  ],
  "inputs": [
    {
      "id": "migrationMessage",
      "description": "Migration message",
      "default": "Auto-generated migration",
      "type": "promptString"
    }
  ]
}
```

## Environment Setup

### 1. Python Interpreter

1. Open Command Palette (`Ctrl+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose your virtual environment Python interpreter

### 2. Environment Variables

Create `.env` file in project root:
```env
# Copy from .env.example and modify as needed
DB_HOST=localhost
DB_PORT=3306
DB_NAME=order_management
# ... other variables
```

### 3. Test Configuration

Create `.env.test` for testing:
```env
DB_NAME=order_management_test
# ... test-specific variables
```

## Development Workflow

### 1. Starting Development

1. **Open Project**:
   - File → Open Folder → Select project directory

2. **Select Python Interpreter**:
   - `Ctrl+Shift+P` → "Python: Select Interpreter"
   - Choose virtual environment interpreter

3. **Start Development Server**:
   - Press `F5` → Select "Launch Server"
   - Or use Command Palette: "Tasks: Run Task" → "Start Development Server"

### 2. Debugging

**Set Breakpoints**:
- Click in the gutter next to line numbers
- Or press `F9` on the line

**Start Debugging**:
- Press `F5` → Select "Launch Server (Debug Mode)"
- Code will pause at breakpoints

**Debug Controls**:
- `F5` - Continue
- `F10` - Step Over
- `F11` - Step Into
- `Shift+F11` - Step Out
- `Ctrl+Shift+F5` - Restart

### 3. Testing

**Run All Tests**:
- Press `F5` → Select "Run Tests"
- Or use Test Explorer in sidebar

**Run Specific Test**:
- Right-click test function → "Run Test"
- Or click the play button next to test

**Debug Tests**:
- Right-click test → "Debug Test"
- Set breakpoints in test code

### 4. Code Formatting and Linting

**Auto-format on Save**:
- Enabled by default in settings
- Uses Black formatter

**Manual Formatting**:
- `Shift+Alt+F` - Format document
- Or Command Palette: "Format Document"

**Linting**:
- Flake8 runs automatically
- Issues shown in Problems panel

## API Development

### 1. REST Client Setup

Create `api-tests.http`:

```http
### Get API Documentation
GET http://localhost:12345/docs

### Health Check
GET http://localhost:12345/health

### Login with Email
POST http://localhost:12345/api/v1/auth/login/email
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}

### Get User Profile
GET http://localhost:12345/api/v1/auth/profile
Authorization: Bearer {{access_token}}

### Create Order
POST http://localhost:12345/api/v1/orders
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "customer_id": "123",
  "items": [
    {
      "product_id": "456",
      "quantity": 2,
      "price": 29.99
    }
  ]
}
```

### 2. Environment Variables for HTTP Files

Create `.vscode/settings.json` addition:

```json
{
  "rest-client.environmentVariables": {
    "local": {
      "baseUrl": "http://localhost:12345",
      "access_token": "your-jwt-token-here"
    },
    "dev": {
      "baseUrl": "https://dev-api.yourcompany.com",
      "access_token": "dev-jwt-token"
    }
  }
}
```

## Database Management

### 1. Database Explorer Extension

Install "SQLite Viewer" or "MySQL" extension for database browsing.

### 2. Migration Workflow

1. **Create Migration**:
   - Command Palette → "Tasks: Run Task" → "Create Migration"
   - Enter migration message

2. **Run Migration**:
   - Command Palette → "Tasks: Run Task" → "Database Migration"

3. **View Migration Status**:
   ```bash
   # In integrated terminal
   alembic current
   alembic history
   ```

## Code Quality

### 1. Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203]
```

### 2. Code Coverage

View coverage in VS Code:
- Install "Coverage Gutters" extension
- Run tests with coverage
- Coverage highlights appear in editor

## Shortcuts and Tips

### Essential Shortcuts

- `Ctrl+Shift+P` - Command Palette
- `Ctrl+P` - Quick Open File
- `Ctrl+Shift+F` - Search in Files
- `Ctrl+`` ` - Toggle Terminal
- `F5` - Start Debugging
- `Ctrl+F5` - Run Without Debugging
- `Shift+Alt+F` - Format Document
- `Ctrl+Shift+I` - Format Selection

### Python-Specific Shortcuts

- `Shift+Enter` - Run Selection in Python Terminal
- `Ctrl+Shift+E` - Explorer
- `Ctrl+Shift+G` - Source Control
- `Ctrl+Shift+D` - Debug
- `Ctrl+Shift+X` - Extensions

### Useful Tips

1. **Multi-cursor Editing**: `Alt+Click` or `Ctrl+Alt+Down`
2. **Duplicate Line**: `Shift+Alt+Down`
3. **Move Line**: `Alt+Up/Down`
4. **Go to Definition**: `F12`
5. **Peek Definition**: `Alt+F12`
6. **Find All References**: `Shift+F12`

## Troubleshooting

### Common Issues

1. **Python Interpreter Not Found**:
   - Check virtual environment activation
   - Verify Python path in settings

2. **Import Errors**:
   - Set PYTHONPATH in launch configuration
   - Check workspace folder structure

3. **Linting Issues**:
   - Verify flake8 installation
   - Check flake8 configuration

4. **Debugging Not Working**:
   - Check launch.json configuration
   - Verify environment variables

5. **Tests Not Discovered**:
   - Check pytest configuration
   - Verify test file naming convention

### Performance Optimization

1. **Exclude Large Directories**:
   ```json
   {
     "files.exclude": {
       "**/node_modules": true,
       "**/.git": true,
       "**/__pycache__": true,
       "**/venv": true,
       "**/env": true
     }
   }
   ```

2. **Disable Unnecessary Extensions**:
   - Disable extensions not needed for Python development

3. **Adjust Python Analysis**:
   ```json
   {
     "python.analysis.autoImportCompletions": true,
     "python.analysis.typeCheckingMode": "basic"
   }
   ```

This setup provides a comprehensive development environment for the Order Management Service with full debugging, testing, and code quality features.
