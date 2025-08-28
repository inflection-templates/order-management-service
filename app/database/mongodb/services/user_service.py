from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.user import UserModel
from app.domain_types.schemas.user import UserCreateModel, UserUpdateModel, UserSearchFilters  # Changed from UserSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBUserService:
    """MongoDB user service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.users
    
    def create_user(self, model: UserCreateModel) -> UserModel:
        """Create a new user"""
        try:
            user_dict = model.model_dump()
            user = UserModel(**user_dict)
            user.update_timestamp()
            
            result = self.collection.insert_one(user.model_dump(by_alias=True))
            user.id = result.inserted_id
            
            logger.info(f"Created user with ID: {user.id}")
            return user.__dict__
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise
    
    def get_user_by_id(self, user_id: str) -> Optional[UserModel]:
        """Get user by ID"""
        try:
            from bson import ObjectId
            user_doc = self.collection.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                return UserModel(**user_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get user by ID {user_id}: {e}")
            raise
    
    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """Get user by email"""
        try:
            user_doc = self.collection.find_one({"email": email.lower()})
            if user_doc:
                return UserModel(**user_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get user by email {email}: {e}")
            raise
    
    def update_user(self, user_id: str, model: UserUpdateModel) -> Optional[UserModel]:
        """Update user"""
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
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete user {user_id}: {e}")
            raise
    
    def search_users(self, search_filter: UserSearchFilters) -> List[UserModel]:  # Changed from UserSearchFilter
        """Search users with filters"""
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
