from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.user_external_auth import UserExternalAuthModel
from app.common.logger import logger
from datetime import datetime

class MongoDBUserExternalAuthService:
    """MongoDB user external authentication service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.user_external_auths
    
    def create_external_auth(self, model: Dict[str, Any]) -> UserExternalAuthModel:
        """Create a new external authentication record"""
        try:
            external_auth = UserExternalAuthModel(**model)
            external_auth.update_timestamp()
            
            result = self.collection.insert_one(external_auth.model_dump(by_alias=True))
            external_auth.id = result.inserted_id
            
            logger.info(f"Created external auth record with ID: {external_auth.id}")
            return external_auth.__dict__
        except Exception as e:
            logger.error(f"Failed to create external auth record: {e}")
            raise
    
    def get_external_auth_by_id(self, auth_id: str) -> Optional[UserExternalAuthModel]:
        """Get external authentication record by ID"""
        try:
            from bson import ObjectId
            auth_doc = self.collection.find_one({"_id": ObjectId(auth_id)})
            if auth_doc:
                return UserExternalAuthModel(**auth_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get external auth by ID {auth_id}: {e}")
            raise
    
    def get_external_auth_by_user_id(self, user_id: str) -> List[UserExternalAuthModel]:
        """Get all external authentication records for a user"""
        try:
            auth_records = []
            cursor = self.collection.find({"user_id": user_id})
            for auth_doc in cursor:
                auth_records.append(UserExternalAuthModel(**auth_doc))
            return auth_records
        except Exception as e:
            logger.error(f"Failed to get external auth records for user {user_id}: {e}")
            raise
    
    def get_external_auth_by_provider(self, user_id: str, provider: str) -> Optional[UserExternalAuthModel]:
        """Get external authentication record for a specific provider and user"""
        try:
            auth_doc = self.collection.find_one({
                "user_id": user_id,
                "provider": provider
            })
            if auth_doc:
                return UserExternalAuthModel(**auth_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get external auth for user {user_id} and provider {provider}: {e}")
            raise
    
    def get_external_auth_by_external_id(self, provider: str, external_user_id: str) -> Optional[UserExternalAuthModel]:
        """Get external authentication record by external provider user ID"""
        try:
            auth_doc = self.collection.find_one({
                "provider": provider,
                "external_user_id": external_user_id
            })
            if auth_doc:
                return UserExternalAuthModel(**auth_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get external auth for provider {provider} and external ID {external_user_id}: {e}")
            raise
    
    def get_external_auth_by_email(self, email: str, provider: Optional[str] = None) -> List[UserExternalAuthModel]:
        """Get external authentication records by email, optionally filtered by provider"""
        try:
            query = {"email": email}
            if provider:
                query["provider"] = provider
                
            auth_records = []
            cursor = self.collection.find(query)
            for auth_doc in cursor:
                auth_records.append(UserExternalAuthModel(**auth_doc))
            return auth_records
        except Exception as e:
            logger.error(f"Failed to get external auth records for email {email}: {e}")
            raise
    
    def update_external_auth(self, auth_id: str, model: Dict[str, Any]) -> Optional[UserExternalAuthModel]:
        """Update external authentication record"""
        try:
            from bson import ObjectId
            model["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(auth_id)},
                {"$set": model}
            )
            
            if result.modified_count > 0:
                return self.get_external_auth_by_id(auth_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update external auth {auth_id}: {e}")
            raise
    
    def update_tokens(self, user_id: str, provider: str, access_token: str, refresh_token: Optional[str] = None, expires_at: Optional[datetime] = None) -> bool:
        """Update access and refresh tokens for a user's external auth"""
        try:
            update_data = {
                "access_token": access_token,
                "updated_at": datetime.utcnow()
            }
            
            if refresh_token:
                update_data["refresh_token"] = refresh_token
            
            if expires_at:
                update_data["token_expires_at"] = expires_at
            
            result = self.collection.update_one(
                {"user_id": user_id, "provider": provider},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update tokens for user {user_id} and provider {provider}: {e}")
            raise
    
    def revoke_tokens(self, user_id: str, provider: str) -> bool:
        """Revoke tokens by setting them to None"""
        try:
            result = self.collection.update_one(
                {"user_id": user_id, "provider": provider},
                {"$set": {
                    "access_token": None,
                    "refresh_token": None,
                    "token_expires_at": None,
                    "updated_at": datetime.utcnow()
                }}
            )
            
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to revoke tokens for user {user_id} and provider {provider}: {e}")
            raise
    
    def delete_external_auth(self, auth_id: str) -> bool:
        """Delete external authentication record"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(auth_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete external auth {auth_id}: {e}")
            raise
    
    def delete_user_external_auths(self, user_id: str) -> bool:
        """Delete all external authentication records for a user"""
        try:
            result = self.collection.delete_many({"user_id": user_id})
            deleted_count = result.deleted_count
            logger.info(f"Deleted {deleted_count} external auth records for user {user_id}")
            return deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete external auth records for user {user_id}: {e}")
            raise
    
    def get_expired_tokens(self) -> List[UserExternalAuthModel]:
        """Get all external auth records with expired tokens"""
        try:
            auth_records = []
            cursor = self.collection.find({
                "token_expires_at": {"$lt": datetime.utcnow()},
                "access_token": {"$ne": None}
            })
            for auth_doc in cursor:
                auth_records.append(UserExternalAuthModel(**auth_doc))
            return auth_records
        except Exception as e:
            logger.error(f"Failed to get expired tokens: {e}")
            raise
    
    def get_all_by_provider(self, provider: str) -> List[UserExternalAuthModel]:
        """Get all external authentication records for a specific provider"""
        try:
            auth_records = []
            cursor = self.collection.find({"provider": provider})
            for auth_doc in cursor:
                auth_records.append(UserExternalAuthModel(**auth_doc))
            return auth_records
        except Exception as e:
            logger.error(f"Failed to get external auth records for provider {provider}: {e}")
            raise
