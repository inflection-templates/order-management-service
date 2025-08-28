from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.tenant import TenantModel
from app.common.logger import logger
from datetime import datetime

class MongoDBTenantService:
    """MongoDB tenant service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.tenants
    
    def create_tenant(self, model: Dict[str, Any]) -> TenantModel:
        """Create a new tenant"""
        try:
            tenant = TenantModel(**model)
            tenant.update_timestamp()
            
            result = self.collection.insert_one(tenant.model_dump(by_alias=True))
            tenant.id = result.inserted_id
            
            logger.info(f"Created tenant with ID: {tenant.id}")
            return tenant.__dict__
        except Exception as e:
            logger.error(f"Failed to create tenant: {e}")
            raise
    
    def get_tenant_by_id(self, tenant_id: str) -> Optional[TenantModel]:
        """Get tenant by ID"""
        try:
            from bson import ObjectId
            tenant_doc = self.collection.find_one({"_id": ObjectId(tenant_id)})
            if tenant_doc:
                return TenantModel(**tenant_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get tenant by ID {tenant_id}: {e}")
            raise
    
    def get_tenant_by_domain(self, domain: str) -> Optional[TenantModel]:
        """Get tenant by domain"""
        try:
            tenant_doc = self.collection.find_one({"domain": domain})
            if tenant_doc:
                return TenantModel(**tenant_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get tenant by domain {domain}: {e}")
            raise
    
    def get_active_tenants(self) -> List[TenantModel]:
        """Get all active tenants"""
        try:
            tenants = []
            cursor = self.collection.find({"is_active": True})
            for tenant_doc in cursor:
                tenants.append(TenantModel(**tenant_doc))
            return tenants
        except Exception as e:
            logger.error(f"Failed to get active tenants: {e}")
            raise
    
    def update_tenant(self, tenant_id: str, model: Dict[str, Any]) -> Optional[TenantModel]:
        """Update tenant"""
        try:
            from bson import ObjectId
            model["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(tenant_id)},
                {"$set": model}
            )
            
            if result.modified_count > 0:
                return self.get_tenant_by_id(tenant_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update tenant {tenant_id}: {e}")
            raise
    
    def delete_tenant(self, tenant_id: str) -> bool:
        """Delete tenant"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(tenant_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete tenant {tenant_id}: {e}")
            raise
