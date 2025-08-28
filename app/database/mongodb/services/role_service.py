from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.role import RoleModel
from app.domain_types.schemas.role import RoleCreateModel, RoleUpdateModel, RoleSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBRoleService:
    """MongoDB role service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.roles
    
    def create_role(self, model: RoleCreateModel) -> RoleModel:
        """Create a new role"""
        try:
            role_dict = model.model_dump()
            role = RoleModel(**role_dict)
            role.update_timestamp()
            
            result = self.collection.insert_one(role.model_dump(by_alias=True))
            role.id = result.inserted_id
            
            logger.info(f"Created role with ID: {role.id}")
            return role.__dict__
        except Exception as e:
            logger.error(f"Failed to create role: {e}")
            raise
    
    def get_role_by_id(self, role_id: str) -> Optional[RoleModel]:
        """Get role by ID"""
        try:
            from bson import ObjectId
            role_doc = self.collection.find_one({"_id": ObjectId(role_id)})
            if role_doc:
                return RoleModel(**role_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get role by ID {role_id}: {e}")
            raise
    
    def update_role(self, role_id: str, model: RoleUpdateModel) -> Optional[RoleModel]:
        """Update role"""
        try:
            from bson import ObjectId
            update_data = model.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(role_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_role_by_id(role_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update role {role_id}: {e}")
            raise
    
    def delete_role(self, role_id: str) -> bool:
        """Delete role"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(role_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete role {role_id}: {e}")
            raise
    
    def search_roles(self, search_filter: RoleSearchFilter) -> List[RoleModel]:
        """Search roles with filters"""
        try:
            query = {}
            
            if search_filter.Name:
                query["Name"] = {"$regex": search_filter.Name, "$options": "i"}
            
            if search_filter.IsActive is not None:
                query["IsActive"] = search_filter.IsActive
            
            cursor = self.collection.find(query)
            roles = [RoleModel(**role_doc) for role_doc in cursor]
            
            return roles
        except Exception as e:
            logger.error(f"Failed to search roles: {e}")
            raise