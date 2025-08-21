from typing import Union, Any
from enum import Enum
from app.config.config import get_settings
import re
import importlib

class ORMType(Enum):
    SQLALCHEMY = "sqlalchemy"
    SQLMODEL = "sqlmodel"

class ORMFactory:
    def __init__(self):
        self.settings = get_settings()
        orm_type_value = self._clean_orm_type(self.settings.ORM_TYPE)
        
        try:
            self._orm_type = ORMType(orm_type_value.lower())
        except ValueError:
            self._orm_type = ORMType.SQLALCHEMY
        
        print(f"🔧 ORM Configuration: {self._orm_type.value.upper()}")
        # Force database initialization
        self._initialize_database()
    
    def _clean_orm_type(self, orm_type_raw: str) -> str:
        cleaned = re.split(r'#', orm_type_raw)[0]
        return cleaned.strip()
    
    def _initialize_database(self):
        """Initialize the selected database immediately"""
        try:
            if self._orm_type == ORMType.SQLALCHEMY:
                # Force import of SQLAlchemy database accessor
                import app.database_alchemy.database_accessor
            elif self._orm_type == ORMType.SQLMODEL:
                # Force import of SQLModel database accessor
                import app.database_sqlmodel.database_accessor
        except Exception as e:
            print(f"❌ Failed to initialize {self._orm_type.value} database: {e}")
    
    @property
    def orm_type(self) -> ORMType:
        return self._orm_type
    
    def get_database_accessor(self):
        if self._orm_type == ORMType.SQLALCHEMY:
            from app.database_alchemy.database_accessor import get_db_session
            return get_db_session
        elif self._orm_type == ORMType.SQLMODEL:
            from app.database_sqlmodel.database_accessor import get_db_session
            return get_db_session
    
    def get_service_module(self, service_name: str):
        try:
            if self._orm_type == ORMType.SQLALCHEMY:
                module_path = f"app.database_alchemy.services.{service_name}"
                return importlib.import_module(module_path)
            elif self._orm_type == ORMType.SQLMODEL:
                module_path = f"app.database_sqlmodel.services.{service_name}"
                return importlib.import_module(module_path)
        except ModuleNotFoundError as e:
            raise ImportError(f"Service '{service_name}' not found in {self._orm_type.value} services") from e

orm_factory = ORMFactory()
