# SQLModel Documentation

## Overview

This document provides comprehensive documentation for the SQLModel implementation in the Order Management Service. SQLModel is a library that combines the best of SQLAlchemy and Pydantic, providing type-safe database operations with modern Python syntax.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Model Definitions](#model-definitions)
3. [Database Services](#database-services)
4. [Database Management](#database-management)
5. [ORM Switching and Multi-ORM Support](#orm-switching-and-multi-orm-support)
6. [Migrations](#migrations)

## Architecture Overview

### Directory Structure

```markdown:docs/sqlmodel-documentation.md
<code_block_to_apply_changes_from>
app/database/sql_model/
├── base.py                 # Base SQLModel configuration
├── database_accessor.py    # Database session management
├── database_initializer.py # Database initialization and table creation
├── models/                 # SQLModel table definitions
│   ├── __init__.py        # Model imports and exports
│   ├── user.py            # User model
│   ├── order.py           # Order model
│   ├── customer.py        # Customer model
│   └── ...                # Other models
└── services/              # Business logic layer
    ├── user_service.py    # User CRUD operations
    ├── order_service.py   # Order CRUD operations
    └── ...                # Other services
```

### Key Components

- **Models**: SQLModel classes that define database tables and relationships
- **Services**: Business logic layer that handles CRUD operations
- **Database Initializer**: Handles database creation and table setup
- **Database Accessor**: Manages database sessions and connections

## Model Definitions

### Base Model Configuration

All models inherit from `SQLModel` and use the `table=True` parameter to indicate they should create database tables.

```python
from sqlmodel import SQLModel, Field
from app.common.utils import generate_uuid4

class BaseModel(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow)
```

### User Model

```python
class User(SQLModel, table=True):
    __tablename__ = "users"
    
    # Primary Key
    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    
    # Foreign Keys
    TenantId: str = Field(foreign_key="tenants.id", max_length=36)
    
    # Basic Information
    Prefix: Optional[str] = Field(default=None, max_length=16)
    FirstName: Optional[str] = Field(default=None, max_length=70)
    MiddleName: Optional[str] = Field(default=None, max_length=70)
    LastName: Optional[str] = Field(default=None, max_length=70)
    Email: Optional[str] = Field(default=None, max_length=512)
    
    # Contact Information
    CountryCode: Optional[str] = Field(default=None, max_length=16)
    Phone: Optional[str] = Field(default=None, max_length=24)
    
    # Authentication
    UserName: Optional[str] = Field(default=None, max_length=128)
    Password: Optional[str] = Field(default=None, max_length=256)
    IsTwoFactorEnabled: bool = Field(default=False)
    IsEmailVerified: bool = Field(default=False)
    IsPhoneVerified: bool = Field(default=False)
    
    # Status
    IsActive: bool = Field(default=True)
    
    # Timestamps
    CreatedAt: datetime = Field(
        default_factory=datetime.utcnow, 
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    UpdatedAt: datetime = Field(
        default_factory=datetime.utcnow, 
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )
    DeletedAt: Optional[datetime] = Field(default=None)
```

### Order Model

```python
class Order(SQLModel, table=True):
    __tablename__ = "orders"
    
    # Primary Key
    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    
    # Order Information
    DisplayCode: str = Field(default=None, index=True, unique=True, max_length=36)
    OrderStatus: OrderStatusTypes = Field(
        default=OrderStatusTypes.DRAFT.value, 
        sa_column_kwargs={"nullable": False}
    )
    InvoiceNumber: Optional[str] = Field(default=None, index=True, unique=True, max_length=64)
    
    # Cart Association
    AssociatedCartId: Optional[str] = Field(default=None, foreign_key="carts.id", max_length=36)
    
    # Order Details
    TotalItemsCount: int = Field(default=0)
    OrderDiscount: float = Field(default=0.0)
    TipApplicable: bool = Field(default=False)
    TipAmount: float = Field(default=0.0)
    TotalTax: float = Field(default=0.0)
    TotalDiscount: float = Field(default=0.0)
    TotalAmount: float = Field(default=0.0)
    
    # Customer and Addresses
    CustomerId: Optional[str] = Field(default=None, foreign_key="customers.id", max_length=36)
    ShippingAddressId: Optional[str] = Field(default=None, foreign_key="addresses.id", max_length=36)
    BillingAddressId: Optional[str] = Field(default=None, foreign_key="addresses.id", max_length=36)
    
    # Order Type
    OrderType: Optional[str] = Field(default=None, foreign_key="order_types.id", max_length=36)
    
    # Timestamps
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: datetime = Field(default_factory=datetime.utcnow)
```

### Customer Model with Relationships

```python
class Customer(SQLModel, table=True):
    __tablename__ = "customers"
    
    # Primary Key
    id: str = Field(default_factory=generate_uuid4, primary_key=True, index=True, max_length=36)
    
    # Basic Information
    ReferenceId: Optional[str] = Field(default=None, unique=True, max_length=36)
    Name: Optional[str] = Field(default=None, max_length=128)
    Email: Optional[str] = Field(default=None, unique=True, max_length=512)
    PhoneCode: Optional[str] = Field(default=None, max_length=8)
    Phone: Optional[str] = Field(default=None, unique=True, max_length=64)
    ProfilePicture: Optional[str] = Field(default=None, max_length=512)
    TaxNumber: Optional[str] = Field(default=None, unique=True, max_length=64)
    
    # Address References
    DefaultShippingAddressId: Optional[str] = Field(
        default=None, foreign_key="addresses.id", max_length=36
    )
    DefaultBillingAddressId: Optional[str] = Field(
        default=None, foreign_key="addresses.id", max_length=36
    )
    
    # Timestamps
    CreatedAt: datetime = Field(default_factory=datetime.utcnow)
    UpdatedAt: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Relationships
    default_shipping_address: Optional[Address] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Customer.DefaultShippingAddressId]", 
            "backref": "customers_shipping"
        }
    )
    default_billing_address: Optional[Address] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[Customer.DefaultBillingAddressId]", 
            "backref": "customers_billing"
        }
    )
```

## Database Services

### Service Layer Pattern

All database operations are encapsulated in service classes that provide a clean interface for business logic.

### User Service

```python
@trace_span("service: create_user")
def create_user(session: Session, model: UserCreateModel) -> UserResponseModel:
    """
    Create a new user with validation and role assignment.
    
    Args:
        session: Database session
        model: User creation model
        
    Returns:
        Created user response model
        
    Raises:
        Conflict: If user with email or phone already exists
    """
    # Check for existing users
    if model.Email:
        existing_user = session.exec(
            select(User).filter(func.lower(User.Email) == func.lower(model.Email))
        ).first()
        if existing_user:
            raise Conflict(f"User with email {model.Email} already exists!")

    if model.Phone:
        existing_user = session.exec(
            select(User).filter(User.Phone == model.Phone)
        ).first()
        if existing_user:
            raise Conflict(f"User with phone {model.Phone} already exists!")
    
    # Hash password and create user
    model.Password = hash_password(model.Password)
    model_dict = model.dict()
    model_dict.pop('RoleId', None)
    db_model = User(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    
    # Save to database
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    
    # Handle role assignment
    if hasattr(model, 'RoleId') and model.RoleId:
        user_role = UserRole(UserId=db_model.id, RoleId=model.RoleId)
        session.add(user_role)
        session.commit()
    
    return db_model.dict()
```

### Order Service

```python
@trace_span("service: search_orders")
def search_orders(session: Session, filter: OrderSearchFilter) -> OrderSearchResults:
    """
    Search orders with advanced filtering, sorting, and pagination.
    
    Args:
        session: Database session
        filter: Search filter criteria
        
    Returns:
        Search results with pagination
    """
    query = select(Order)
    
    # Apply filters
    if filter.CustomerId:
        query = query.where(Order.CustomerId.like(f'%{filter.CustomerId}%'))
    if filter.AssociatedCartId:
        query = query.where(Order.AssociatedCartId.like(f'%{filter.AssociatedCartId}%'))
    if filter.TotalItemsCountGreaterThan:
        query = query.where(Order.TotalItemsCount > filter.TotalItemsCountGreaterThan)
    if filter.TotalAmountGreaterThan:
        query = query.where(Order.TotalAmount > filter.TotalAmountGreaterThan)
    if filter.OrderStatus:
        query = query.where(Order.OrderStatus == filter.OrderStatus)
    if filter.CreatedBefore:
        query = query.where(Order.CreatedAt < filter.CreatedBefore)
    if filter.CreatedAfter:
        query = query.where(Order.CreatedAt > filter.CreatedAfter)
    
    # Apply sorting
    if filter.OrderBy and hasattr(Order, filter.OrderBy):
        order_by = getattr(Order, filter.OrderBy)
        if filter.SortOrder and filter.SortOrder.lower() == 'desc':
            query = query.order_by(desc(order_by))
        else:
            query = query.order_by(asc(order_by))
    
    # Apply pagination
    total_count = len(session.exec(query).all())
    if filter.PageSize and filter.PageNumber:
        offset = (filter.PageNumber - 1) * filter.PageSize
        query = query.offset(offset).limit(filter.PageSize)
    
    orders = session.exec(query).all()
    
    return OrderSearchResults(
        items=orders,
        total_count=total_count,
        page_number=filter.PageNumber or 1,
        page_size=filter.PageSize or total_count
    )
```

## Database Management

### Database Initialization

The database initializer handles automatic database creation and table setup.

```python
def initialize_database() -> bool:
    """
    Initialize the database by creating it if it doesn't exist.
    
    Returns:
        True if successful, False otherwise
    """
    global _database_initialized
    
    if _database_initialized:
        logger.debug("[SQLModel] Database already initialized, skipping...")
        return True
    
    settings = get_settings()
    
    try:
        # Create connection to MySQL server without specifying database
        server_connection_string = f"{settings.DB_DIALECT}+{settings.DB_DRIVER}://{settings.DB_USER_NAME}:{settings.DB_USER_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"
        
        # Create engine for server connection
        server_engine = create_engine(server_connection_string, echo=False)
        
        # Check if database exists and create if needed
        with server_engine.connect() as connection:
            result = connection.execute(
                text(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{settings.DB_NAME}'")
            )
            
            if result.fetchone() is None:
                logger.info(f"[SQLModel] Database '{settings.DB_NAME}' not found. Creating...")
                connection.execute(text(f"CREATE DATABASE {settings.DB_NAME}"))
                connection.commit()
                logger.info(f"[SQLModel] Database '{settings.DB_NAME}' created successfully!")
            else:
                logger.info(f"[SQLModel] Database '{settings.DB_NAME}' already exists")
        
        server_engine.dispose()
        _database_initialized = True
        return True
        
    except Exception as e:
        logger.error(f"[SQLModel] Database initialization failed: {e}")
        return False
```

### Table Creation

```python
def create_tables_if_not_exist():
    """
    Create all tables if they don't exist.
    This function imports all models and creates the tables.
    """
    global _tables_created
    
    if _tables_created:
        return True
    
    try:
        from sqlmodel import SQLModel, create_engine
        from app.config.config import get_settings
        
        # Import all models to ensure they're registered with SQLModel
        from app.database.sql_model.models import (
            Address, AuthToken, Cart, Coupon, Customer, Merchant, Order,
            OrderCoupon, OrderLineItem, OrderType, OrderHistory,
            PaymentTransaction, Role, Tenant, User, UserRole, customer_address
        )
        
        settings = get_settings()
        engine = create_engine(settings.DB_CONNECTION_STRING, echo=False)
        
        # Create all tables
        SQLModel.metadata.create_all(bind=engine)
        
        engine.dispose()
        _tables_created = True
        return True
        
    except Exception as e:
        logger.error(f"[SQLModel] Failed to create tables: {e}")
        return False
```

### Database Session Management

```python
from sqlmodel import SQLModel, create_engine, Session
from app.config.config import get_settings

# Load config
settings = get_settings()

# Create the engine
engine = create_engine(settings.DB_CONNECTION_STRING, echo=False)

def get_db_session() -> Session:
    """
    Get a new database session.
    
    Returns:
        SQLModel database session
    """
    return Session(engine)
```

## ORM Switching and Multi-ORM Support

The Order Management Service supports multiple ORMs and databases through a sophisticated factory pattern, allowing seamless switching between different database technologies without changing application code.

### Architecture Overview

The system uses a layered approach with:
- **Database Factory**: Manages ORM selection and initialization
- **Database Interface**: Provides unified access to services across ORMs
- **Service Layer**: Business logic that works with any ORM
- **Model Layer**: ORM-specific model definitions

### Configuration

ORM switching is controlled through environment variables:

```bash
# Database type selection
DB_DIALECT=mysql          # Options: "mysql", "mongodb"

# ORM selection (only applies to MySQL)
ORM_TYPE=sqlmodel         # Options: "sqlmodel", "sqlalchemy"

# Database connection details
DB_HOST=localhost
DB_PORT=3306
DB_NAME=order_management
DB_USER_NAME=dbuser
DB_USER_PASSWORD=dbpassword
```

### Factory Pattern Implementation

The `DatabaseFactory` class automatically detects and initializes the appropriate database and ORM:

```python
from app.database.orm_factory import database_factory

class DatabaseFactory:
    """Factory class to handle database and ORM switching"""
    
    def __init__(self):
        self.settings = get_settings()
        
        # Clean the DB_DIALECT value
        db_dialect_value = self._clean_value(self.settings.DB_DIALECT)
        orm_type_value = self._clean_value(self.settings.ORM_TYPE)
        
        # Determine database type
        self._database_type = DatabaseType(db_dialect_value.lower())
        
        # ORM type only applies to MySQL
        if self._database_type == DatabaseType.MYSQL:
            self._orm_type = ORMType(orm_type_value.lower())
        else:
            self._orm_type = None
        
        # Initialize the selected database
        self._initialize_database()
    
    def _initialize_mysql(self):
        """Initialize MySQL database with selected ORM"""
        if self._orm_type == ORMType.SQLMODEL:
            from app.database.sql_model.database_initializer import initialize_database
            initialize_database()
        elif self._orm_type == ORMType.SQLALCHEMY:
            from app.database.sql_alchemy.database_initializer import initialize_database
            initialize_database()
```

### Unified Database Interface

The `DatabaseInterface` class provides a consistent API regardless of the underlying ORM:

```python
from app.database.database_interface import db_interface

class DatabaseInterface:
    """Unified interface for database operations across ORMs"""
    
    def get_order_service(self):
        """Get order service for the active ORM"""
        return self._get_service("order_service")
    
    def get_customer_service(self):
        """Get customer service for the active ORM"""
        return self._get_service("customer_service")
    
    def get_db_session(self):
        """Get database session for the active database"""
        return self.database_factory.get_database_accessor()
```

### Service Layer Abstraction

Services automatically use the correct ORM through the factory pattern:

```python
# This code works with any ORM without changes
from app.database.database_interface import db_interface

def create_order(order_data: dict):
    """Create order using the active ORM"""
    order_service = db_interface.get_order_service()
    session = db_interface.get_db_session()
    
    # The service automatically uses SQLModel, SQLAlchemy, or MongoDB
    return order_service.create_order(session, order_data)
```

### Switching Between ORMs

#### 1. Environment Variable Method

```bash
# Switch to SQLModel
export ORM_TYPE=sqlmodel
export DB_DIALECT=mysql

# Switch to SQLAlchemy
export ORM_TYPE=sqlalchemy
export DB_DIALECT=mysql

# Switch to MongoDB
export DB_DIALECT=mongodb
# ORM_TYPE is ignored for MongoDB
```

#### 3. Runtime Detection

The system automatically detects configuration changes and reinitializes:

```python
# The factory automatically handles ORM switching
database_factory = DatabaseFactory()

# Check current configuration
print(f"Database: {database_factory.database_type.value}")
print(f"ORM: {database_factory.orm_type.value if database_factory.orm_type else 'N/A'}")

# Get appropriate services
order_service = database_factory.get_service_module("order_service")
```

### Migration Management

Each ORM has its own migration system:

#### SQLModel Migrations
```bash
# Use SQLModel-specific Alembic configuration
alembic -c alembic_sqlmodel.ini upgrade head
```

#### SQLAlchemy Migrations
```bash
# Use SQLAlchemy-specific Alembic configuration
alembic -c alembic.ini upgrade head
```

#### MongoDB Migrations
```python
# MongoDB uses native migration scripts
from app.database.mongodb.migration_manager import run_migrations
run_migrations()
```

## Migrations

### Alembic Integration

The service uses Alembic for database migrations, which automatically generates SQL from SQLModel definitions.

### Migration Structure

```
alembic_sqlmodel/
├── env.py                 # Alembic environment configuration
├── script.py.mako        # Migration template
├── alembic.ini          # Alembic configuration
└── versions/             # Migration files
    ├── d14c558219f8_initial_migration.py
    ├── 74d1a21ca61b_initial_migration_latest_codes.py
    └── ...
```

## Conclusion

This SQLModel implementation provides a robust, type-safe foundation for database operations in the Order Management Service. By following the patterns and best practices outlined in this documentation, developers can efficiently work with the database layer while maintaining code quality and performance.

For additional information, refer to:
- [SQLModel Official Documentation](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
```