from typing import Union, Any
from enum import Enum
from app.config.config import get_settings
import re
import importlib

class DatabaseType(Enum):
    MYSQL = "mysql"
    MONGODB = "mongodb"

class ORMType(Enum):
    SQLALCHEMY = "sqlalchemy"
    SQLMODEL = "sqlmodel"

class DatabaseFactory:
    """Factory class to handle database and ORM switching"""
    
    def __init__(self):
        self.settings = get_settings()
        
        # Clean the DB_DIALECT value (replaces DATABASE_TYPE)
        db_dialect_value = self._clean_value(self.settings.DB_DIALECT)
        orm_type_value = self._clean_value(self.settings.ORM_TYPE)
        
        try:
            self._database_type = DatabaseType(db_dialect_value.lower())
        except ValueError as e:
            print(f"⚠️  Invalid DB_DIALECT '{db_dialect_value}'. Valid options are: {[db.value for db in DatabaseType]}")
            print(f"   Falling back to default: {DatabaseType.MYSQL.value}")
            self._database_type = DatabaseType.MYSQL
        
        # ORM type only applies to MySQL
        if self._database_type == DatabaseType.MYSQL:
            try:
                self._orm_type = ORMType(orm_type_value.lower())
            except ValueError as e:
                print(f"⚠️  Invalid ORM_TYPE '{orm_type_value}'. Valid options are: {[orm.value for orm in ORMType]}")
                print(f"   Falling back to default: {ORMType.SQLALCHEMY.value}")
                self._orm_type = ORMType.SQLALCHEMY
        else:
            self._orm_type = None
        
        # Print configuration
        print(f"Database Configuration: {self._database_type.value.upper()}")
        if self._orm_type:
            print(f"ORM Configuration: {self._orm_type.value.upper()}")
        
        # Initialize the selected database
        self._initialize_database()
    
    def _clean_value(self, value_raw: str) -> str:
        """Clean configuration value by removing comments and extra whitespace"""
        if not value_raw:
            return ""
        # Remove everything after # (comments)
        cleaned = re.split(r'#', value_raw)[0]
        # Strip whitespace
        cleaned = cleaned.strip()
        return cleaned
    
    def _initialize_database(self):
        """Initialize database setup for the selected database type"""
        try:
            if self._database_type == DatabaseType.MYSQL:
                self._initialize_mysql()
            elif self._database_type == DatabaseType.MONGODB:
                self._initialize_mongodb()
        except Exception as e:
            print(f"Failed to initialize {self._database_type.value} database: {e}")
    
    def _initialize_mysql(self):
        """Initialize MySQL database with selected ORM"""
        if self._orm_type == ORMType.SQLALCHEMY:
            from app.database.sql_alchemy.database_initializer import initialize_database, create_tables_if_not_exist
            if initialize_database():
                print("[MySQL + SQLAlchemy] Database initialized successfully")
                if create_tables_if_not_exist():
                    print("[MySQL + SQLAlchemy] Tables created successfully")
                else:
                    print("[MySQL + SQLAlchemy] Failed to create tables")
            else:
                print("[MySQL + SQLAlchemy] Failed to initialize database")
            from app.database.sql_alchemy import database_accessor
        elif self._orm_type == ORMType.SQLMODEL:
            from app.database.sql_model.database_initializer import initialize_database, create_tables_if_not_exist
            if initialize_database():
                print("[MySQL + SQLModel] Database initialized successfully")
                if create_tables_if_not_exist():
                    print("[MySQL + SQLModel] Tables created successfully")
                else:
                    print("[MySQL + SQLModel] Failed to create tables")
            else:
                print("[MySQL + SQLModel] Failed to initialize database")
            from app.database.sql_model import database_accessor
    
    def _initialize_mongodb(self):
        """Initialize MongoDB database"""
        from app.database.mongodb.database_initializer import initialize_database
        if initialize_database():
            print("[MongoDB] Database initialized successfully")
        else:
            print("[MongoDB] Failed to initialize database")
        from app.database.mongodb import database_accessor
    
    @property
    def database_type(self) -> DatabaseType:
        return self._database_type
    
    @property
    def orm_type(self) -> Union[ORMType, None]:
        return self._orm_type
    
    def get_database_accessor(self):
        """Get the appropriate database accessor based on database type"""
        if self._database_type == DatabaseType.MYSQL:
            if self._orm_type == ORMType.SQLALCHEMY:
                from app.database.sql_alchemy.database_accessor import get_db_session
                return get_db_session
            elif self._orm_type == ORMType.SQLMODEL:
                from app.database.sql_model.database_accessor import get_db_session
                return get_db_session
        elif self._database_type == DatabaseType.MONGODB:
            from app.database.mongodb.database_accessor import get_db_session
            return get_db_session
        
        raise ValueError(f"Unsupported database/ORM combination: {self._database_type.value}/{self._orm_type.value if self._orm_type else 'N/A'}")
    
    def get_service_module(self, service_name: str):
        """Get the appropriate service module based on database type"""
        try:
            if self._database_type == DatabaseType.MYSQL:
                if self._orm_type == ORMType.SQLALCHEMY:
                    module_path = f"app.database.sql_alchemy.services.{service_name}"
                elif self._orm_type == ORMType.SQLMODEL:
                    module_path = f"app.database.sql_model.services.{service_name}"
                else:
                    raise ValueError(f"ORM type not set for MySQL")
            elif self._database_type == DatabaseType.MONGODB:
                module_path = f"app.database.mongodb.services.{service_name}"
            else:
                raise ValueError(f"Unsupported database type: {self._database_type.value}")
            
            return importlib.import_module(module_path)
        except ModuleNotFoundError as e:
            raise ImportError(f"Service '{service_name}' not found in {self._database_type.value} services: {module_path}") from e

# Global database factory instance
database_factory = DatabaseFactory()
