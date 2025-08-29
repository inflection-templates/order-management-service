# MongoDB Documentation

## Overview

This document provides comprehensive documentation for the MongoDB implementation in the Order Management Service. The service supports both MySQL and MongoDB databases, with MongoDB providing a flexible document-based storage solution.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Setup & Configuration](#setup--configuration)
3. [Database Models](#database-models)
4. [Services Layer](#services-layer)
5. [API Integration](#api-integration)
6. [Database Operations](#database-operations)

## Architecture Overview

The MongoDB implementation follows a layered architecture:

```
┌─────────────────┐
│   API Layer     │  ← FastAPI endpoints
├─────────────────┤
│  Service Layer  │  ← Business logic & MongoDB operations
├─────────────────┤
│  Model Layer    │  ← Pydantic models & MongoDB schemas
├─────────────────┤
│ Database Layer  │  ← PyMongo connection & operations
└─────────────────┘
```

### Key Components

- **MongoDBInitializer**: Manages database connections and initialization
- **MongoDBBaseModel**: Base class for all MongoDB documents
- **Service Classes**: Handle business logic and database operations
- **Database Factory**: Provides database abstraction and switching

## Setup & Configuration

### Environment Variables

Configure MongoDB in your environment:

```bash
# Database Type Selection
DB_DIALECT=mongodb

# MongoDB Connection
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=order_management

# Connection Pool Settings
MONGODB_MAX_POOL_SIZE=100
MONGODB_MIN_POOL_SIZE=0
MONGODB_MAX_IDLE_TIME_MS=30000
MONGODB_CONNECT_TIMEOUT_MS=20000
MONGODB_SERVER_SELECTION_TIMEOUT_MS=5000
```

### Dependencies

Required Python packages:

```bash
pip install pymongo pydantic
```

## Database Models

### Base Model

All MongoDB models inherit from `MongoDBBaseModel`:

```python
from app.database.mongodb.models.base_model import MongoDBBaseModel

class MongoDBBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
```

### Business Models

#### User Model

```python
class UserModel(MongoDBBaseModel):
    email: EmailStr = Field(..., unique=True, index=True)
    username: Optional[str] = Field(None, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    password_hash: Optional[str] = Field(None)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    tenant_id: Optional[str] = Field(default="default")
    roles: List[str] = Field(default=[])
    failed_login_attempts: int = Field(default=0)
    locked_until: Optional[datetime] = Field(None)
```

#### Order Model

```python
class OrderModel(MongoDBBaseModel):
    DisplayCode: Optional[str] = Field(None, max_length=64)
    InvoiceNumber: Optional[str] = Field(None)
    OrderType: Optional[str] = Field(None, max_length=64)
    CustomerId: str = Field(...)
    AssociatedCartId: Optional[str] = Field(None)
    TotalItemsCount: int = Field(default=0, ge=0, le=100)
    OrderDiscount: float = Field(default=0.0, ge=0.0)
    TipApplicable: bool = Field(default=False)
    TipAmount: float = Field(default=0.0, ge=0.0)
    TotalTax: float = Field(default=0.0, ge=0.0)
    TotalDiscount: float = Field(default=0.0, ge=0.0)
    TotalAmount: float = Field(default=0.0, ge=0.0)
    Notes: Optional[str] = Field(None, max_length=1024)
    Coupons: Optional[List[str]] = Field(default=[])
    OrderStatus: OrderStatusTypes = Field(default=OrderStatusTypes.DRAFT)
```

## Services Layer

### Service Base Pattern

All MongoDB services follow a consistent pattern:

```python
class MongoDBUserService:
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.users
    
    def create_user(self, model: UserCreateModel) -> UserModel:
        # Implementation
    
    def get_user_by_id(self, user_id: str) -> Optional[UserModel]:
        # Implementation
    
    def update_user(self, user_id: str, model: UserUpdateModel) -> Optional[UserModel]:
        # Implementation
    
    def delete_user(self, user_id: str) -> bool:
        # Implementation
    
    def search_users(self, search_filter: UserSearchFilters) -> List[UserModel]:
        # Implementation
```

## API Integration

### Database Interface

The service uses a unified database interface:

```python
from app.database.database_interface import db_interface

# Get MongoDB services
user_service = db_interface.get_user_service()
order_service = db_interface.get_order_service()
```

### API Routes

All API endpoints automatically use MongoDB when configured:

```python
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(model: UserCreateModel, db_session=Depends(get_db_session)):
    return create_user_(model, db_session)
```

## Database Operations

### CRUD Operations

#### Create

```python
def create_user(self, model: UserCreateModel) -> UserModel:
    try:
        user_dict = model.model_dump()
        user = UserModel(**user_dict)
        user.update_timestamp()
        
        result = self.collection.insert_one(user.model_dump(by_alias=True))
        user.id = result.inserted_id
        
        return user.__dict__
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        raise
```

#### Read

```python
def get_user_by_id(self, user_id: str) -> Optional[UserModel]:
    try:
        from bson import ObjectId
        user_doc = self.collection.find_one({"_id": ObjectId(user_id)})
        if user_doc:
            return UserModel(**user_doc)
        return None
    except Exception as e:
        logger.error(f"Failed to get user by ID {user_id}: {e}")
        raise
```

#### Update

```python
def update_user(self, user_id: str, model: UserUpdateModel) -> Optional[UserModel]:
    try:
        from bson import ObjectId
        update_data = model.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return self.get_user_by_id(user_id)
        return None
    except Exception as e:
        logger.error(f"Failed to update user {user_id}: {e}")
        raise
```

#### Delete

```python
def delete_user(self, user_id: str) -> bool:
    try:
        from bson import ObjectId
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Failed to delete user {user_id}: {e}")
        raise
```

### Search Operations

```python
def search_users(self, search_filter: UserSearchFilters) -> List[UserModel]:
    try:
        query = {}
        
        if search_filter.Email:
            query["email"] = {"$regex": search_filter.Email, "$options": "i"}
        
        if search_filter.Phone:
            query["phone"] = {"$regex": search_filter.Phone, "$options": "i"}
        
        if search_filter.RoleId:
            query["role_id"] = search_filter.RoleId
        
        if search_filter.UserName:
            query["username"] = {"$regex": search_filter.UserName, "$options": "i"}
        
        cursor = self.collection.find(query)
        users = [UserModel(**user_doc) for user_doc in cursor]
        
        return users
    except Exception as e:
        logger.error(f"Failed to search users: {e}")
        raise
```

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Migration Guide

### Switching from MySQL to MongoDB

1. Update environment variables:
   ```bash
   DB_DIALECT=mongodb
   ```

2. Ensure MongoDB is running and accessible

3. The system will automatically:
   - Initialize MongoDB connection
   - Create necessary collections
   - Switch service implementations

## Monitoring & Metrics

### Connection Pool Monitoring

```python
# Monitor connection pool status
def get_connection_pool_status():
    client = get_client()
    pool_stats = client.admin.command('serverStatus')
    return pool_stats.get('connections', {})
```

## Security Considerations

### Authentication

- Use MongoDB authentication
- Implement role-based access control
- Secure connection strings

## Conclusion

This MongoDB implementation provides a robust, scalable foundation for the Order Management Service. It follows modern Python practices and provides flexibility for different deployment scenarios.

For additional support or questions, refer to:
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Manual](https://docs.mongodb.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)