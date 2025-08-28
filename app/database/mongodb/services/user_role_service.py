from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.user_role import UserRoleModel
from app.common.logger import logger
from datetime import datetime

class MongoDBUserRoleService:
    """MongoDB user-role service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.user_roles
    
    def create_user_role(self, model: Dict[str, Any]) -> UserRoleModel:
        """Create a new user-role relationship"""
        try:
            user_role = UserRoleModel(**model)
            user_role.update_timestamp()
            
            result = self.collection.insert_one(user_role.model_dump(by_alias=True))
            user_role.id = result.inserted_id
            
            logger.info(f"Created user-role relationship with ID: {user_role.id}")
            return user_role.__dict__
        except Exception as e:
            logger.error(f"Failed to create user-role relationship: {e}")
            raise
    
    def get_user_role_by_id(self, user_role_id: str) -> Optional[UserRoleModel]:
        """Get user-role relationship by ID"""
        try:
            from bson import ObjectId
            user_role_doc = self.collection.find_one({"_id": ObjectId(user_role_id)})
            if user_role_doc:
                return UserRoleModel(**user_role_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get user-role by ID {user_role_id}: {e}")
            raise
    
    def get_user_roles_by_user_id(self, user_id: str) -> List[UserRoleModel]:
        """Get all roles for a specific user"""
        try:
            user_roles = []
            cursor = self.collection.find({
                "user_id": user_id,
                "deleted_at": None  # Only active relationships
            })
            for user_role_doc in cursor:
                user_roles.append(UserRoleModel(**user_role_doc))
            return user_roles
        except Exception as e:
            logger.error(f"Failed to get user roles for user {user_id}: {e}")
            raise
    
    def get_user_roles_by_role_id(self, role_id: int) -> List[UserRoleModel]:
        """Get all users for a specific role"""
        try:
            user_roles = []
            cursor = self.collection.find({
                "role_id": role_id,
                "deleted_at": None  # Only active relationships
            })
            for user_role_doc in cursor:
                user_roles.append(UserRoleModel(**user_role_doc))
            return user_roles
        except Exception as e:
            logger.error(f"Failed to get users for role {role_id}: {e}")
            raise
    
    def check_user_has_role(self, user_id: str, role_id: int) -> bool:
        """Check if a user has a specific role"""
        try:
            user_role_doc = self.collection.find_one({
                "user_id": user_id,
                "role_id": role_id,
                "deleted_at": None
            })
            return user_role_doc is not None
        except Exception as e:
            logger.error(f"Failed to check if user {user_id} has role {role_id}: {e}")
            raise
    
    def add_role_to_user(self, user_id: str, role_id: int) -> UserRoleModel:
        """Add a role to a user"""
        try:
            # Check if relationship already exists
            existing = self.collection.find_one({
                "user_id": user_id,
                "role_id": role_id
            })
            
            if existing:
                if existing.get("deleted_at"):
                    # Reactivate soft-deleted relationship
                    self.collection.update_one(
                        {"_id": existing["_id"]},
                        {"$set": {"deleted_at": None, "updated_at": datetime.utcnow()}}
                    )
                    return UserRoleModel(**existing)
                else:
                    # Relationship already exists and active
                    return UserRoleModel(**existing)
            else:
                # Create new relationship
                return self.create_user_role({
                    "user_id": user_id,
                    "role_id": role_id
                })
        except Exception as e:
            logger.error(f"Failed to add role {role_id} to user {user_id}: {e}")
            raise
    
    def remove_role_from_user(self, user_id: str, role_id: int) -> bool:
        """Remove a role from a user (soft delete)"""
        try:
            result = self.collection.update_one(
                {"user_id": user_id, "role_id": role_id},
                {"$set": {"deleted_at": datetime.utcnow(), "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to remove role {role_id} from user {user_id}: {e}")
            raise
    
    def update_user_role(self, user_role_id: str, model: Dict[str, Any]) -> Optional[UserRoleModel]:
        """Update user-role relationship"""
        try:
            from bson import ObjectId
            model["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(user_role_id)},
                {"$set": model}
            )
            
            if result.modified_count > 0:
                return self.get_user_role_by_id(user_role_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update user-role {user_role_id}: {e}")
            raise
    
    def delete_user_role(self, user_role_id: str) -> bool:
        """Hard delete a user-role relationship"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(user_role_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete user-role {user_role_id}: {e}")
            raise
    
    def get_all_active_user_roles(self) -> List[UserRoleModel]:
        """Get all active user-role relationships"""
        try:
            user_roles = []
            cursor = self.collection.find({"deleted_at": None})
            for user_role_doc in cursor:
                user_roles.append(UserRoleModel(**user_role_doc))
            return user_roles
        except Exception as e:
            logger.error(f"Failed to get all active user roles: {e}")
            raise
