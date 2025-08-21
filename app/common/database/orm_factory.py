from typing import Union, Any
from enum import Enum
from app.config.config import get_settings
import re
import importlib

class ORMType(Enum):
    SQLALCHEMY = "sqlalchemy"
    SQLMODEL = "sqlmodel"

class ORMFactory:
    """Factory class to handle ORM switching"""
    
    def __init__(self):
        self.settings = get_settings()
        # Clean the ORM_TYPE value to remove comments and whitespace
        orm_type_value = self._clean_orm_type(self.settings.ORM_TYPE)
        
        try:
            self._orm_type = ORMType(orm_type_value.lower())
        except ValueError as e:
            print(f"⚠️  Invalid ORM_TYPE '{orm_type_value}'. Valid options are: {[orm.value for orm in ORMType]}")
            print(f"   Falling back to default: {ORMType.SQLALCHEMY.value}")
            self._orm_type = ORMType.SQLALCHEMY
        
        # Print ORM configuration first
        print(f"🔧 ORM Configuration: {self._orm_type.value.upper()}")
        
        # Initialize ONLY the selected database
        self._initialize_database()
    
    def _clean_orm_type(self, orm_type_raw: str) -> str:
        """Clean ORM type value by removing comments and extra whitespace"""
        # Remove everything after # (comments)
        cleaned = re.split(r'#', orm_type_raw)[0]
        # Strip whitespace
        cleaned = cleaned.strip()
        return cleaned
    
    def _initialize_database(self):
        """Initialize database setup ONLY for the selected ORM type"""
        try:
            if self._orm_type == ORMType.SQLALCHEMY:
                # Initialize database and tables for SQLAlchemy
                from app.database_alchemy.database_initializer import initialize_database, create_tables_if_not_exist
                if initialize_database():
                    print("✅ [SQLAlchemy] Database initialized successfully")
                    if create_tables_if_not_exist():
                        print("✅ [SQLAlchemy] Tables created successfully")
                    else:
                        print("❌ [SQLAlchemy] Failed to create tables")
                else:
                    print("❌ [SQLAlchemy] Failed to initialize database")
                # Import database accessor to complete setup
                from app.database_alchemy import database_accessor
            elif self._orm_type == ORMType.SQLMODEL:
                # Initialize database and tables for SQLModel
                from app.database_sqlmodel.database_initializer import initialize_database, create_tables_if_not_exist
                if initialize_database():
                    print("✅ [SQLModel] Database initialized successfully")
                    if create_tables_if_not_exist():
                        print("✅ [SQLModel] Tables created successfully")
                    else:
                        print("❌ [SQLModel] Failed to create tables")
                else:
                    print("❌ [SQLModel] Failed to initialize database")
                # Import database accessor to complete setup
                from app.database_sqlmodel import database_accessor
        except Exception as e:
            print(f"❌ Failed to initialize {self._orm_type.value} database: {e}")
    
    @property
    def orm_type(self) -> ORMType:
        return self._orm_type
    
    def get_database_accessor(self):
        """Get the appropriate database accessor based on ORM type"""
        if self._orm_type == ORMType.SQLALCHEMY:
            from app.database_alchemy.database_accessor import get_db_session
            return get_db_session
        elif self._orm_type == ORMType.SQLMODEL:
            from app.database_sqlmodel.database_accessor import get_db_session
            return get_db_session
        else:
            raise ValueError(f"Unsupported ORM type: {self._orm_type}")
    
    def get_service_module(self, service_name: str):
        """Get the appropriate service module based on ORM type"""
        try:
            if self._orm_type == ORMType.SQLALCHEMY:
                module_path = f"app.database_alchemy.services.{service_name}"
                return importlib.import_module(module_path)
            elif self._orm_type == ORMType.SQLMODEL:
                module_path = f"app.database_sqlmodel.services.{service_name}"
                return importlib.import_module(module_path)
            else:
                raise ValueError(f"Unsupported ORM type: {self._orm_type}")
        except ModuleNotFoundError as e:
            raise ImportError(f"Service '{service_name}' not found in {self._orm_type.value} services: {module_path}") from e

# Global factory instance
orm_factory = ORMFactory()
