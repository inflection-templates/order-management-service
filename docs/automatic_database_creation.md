# Automatic Database Creation

This document explains how the automatic database creation feature works in the Order Management Service.

## Overview

The application now automatically creates the database and tables when it starts up, eliminating the need for manual database setup.

## How It Works

### 1. Database Initialization Flow

When the application starts:

1. **ORM Factory Initialization**: The `ORMFactory` class in `app/common/database/orm_factory.py` is initialized
2. **Database Creation**: The appropriate database initializer is called based on your ORM type (SQLAlchemy or SQLModel)
3. **Table Creation**: All database tables are created automatically
4. **Connection Setup**: Database connections are established and ready for use

### 2. Configuration

The database creation uses the settings from your configuration file (`app/config/config.py`):

```python
# Database Configuration
DB_USER_NAME: str = "dbuser"
DB_USER_PASSWORD: str = "dbpassword"
DB_HOST: str = "localhost"
DB_PORT: int = 3306
DB_NAME: str = "order_management"
DB_DIALECT: str = "mysql"
DB_DRIVER: str = "pymysql"
```

### 3. ORM Support

The automatic database creation works with both ORM types:

- **SQLAlchemy**: Uses `app/database_alchemy/database_initializer.py`
- **SQLModel**: Uses `app/database_sqlmodel/database_initializer.py`

You can switch between ORMs by changing the `ORM_TYPE` setting in your configuration.

## Prerequisites

Before running the application, ensure:

1. **MySQL Server is Running**: The MySQL/MariaDB server must be accessible
2. **Database User Exists**: The database user specified in your config must exist and have the necessary privileges:
   - `CREATE DATABASE` privilege
   - `CREATE TABLE` privilege
   - `INSERT`, `UPDATE`, `DELETE`, `SELECT` privileges on the target database

## Database User Privileges

Your database user needs these minimum privileges:

```sql
-- Grant necessary privileges to your database user
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT ON *.* TO 'dbuser'@'localhost';

-- Or more specifically for your database:
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT ON order_management.* TO 'dbuser'@'localhost';

-- Allow creating databases
GRANT CREATE ON *.* TO 'dbuser'@'localhost';

FLUSH PRIVILEGES;
```

## Testing the Setup

You can test the automatic database creation using the provided test script:

```bash
python test_db_creation.py
```

This script will:
- Initialize the ORM factory
- Attempt to create the database if it doesn't exist
- Create all necessary tables
- Test the database connection
- Report the results

## Environment Variables

You can override the default database settings using environment variables or a `.env` file:

```bash
# .env file example
DB_HOST=localhost
DB_PORT=3306
DB_NAME=order_management
DB_USER_NAME=your_username
DB_USER_PASSWORD=your_password
```

## Logging

The database initialization process provides detailed logging:

- ✅ Success messages for each step
- ❌ Error messages with details if something fails
- 🔧 Configuration information

## Troubleshooting

### Common Issues

1. **Connection Failed**: Check if MySQL server is running and credentials are correct
2. **Permission Denied**: Ensure your database user has the necessary privileges
3. **Database Already Exists**: This is normal - the system will use the existing database
4. **Import Errors**: Make sure all required Python packages are installed

### Error Messages

- `Failed to connect to MySQL server`: Check server status and connection settings
- `Failed to create database`: Check user privileges
- `Failed to create tables`: Check user permissions on the specific database

## Files Modified

The following files implement the automatic database creation:

- `app/common/database/orm_factory.py`: Main orchestration logic
- `app/database_alchemy/database_initializer.py`: SQLAlchemy-specific initialization
- `app/database_sqlmodel/database_initializer.py`: SQLModel-specific initialization
- `app/database_alchemy/database_accessor.py`: SQLAlchemy database access (updated)
- `app/database_sqlmodel/database_accessor.py`: SQLModel database access (updated)

## Benefits

- **Zero Manual Setup**: No need to manually create databases or run migration scripts
- **Environment Agnostic**: Works in development, testing, and production environments
- **Error Handling**: Graceful handling of connection and permission issues
- **Idempotent**: Safe to run multiple times - won't recreate existing databases/tables
- **ORM Agnostic**: Works with both SQLAlchemy and SQLModel
