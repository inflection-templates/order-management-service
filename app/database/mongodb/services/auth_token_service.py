from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.auth_token import AuthTokenModel
from app.common.logger import logger
from datetime import datetime

class MongoDBAuthTokenService:
    """MongoDB authentication token service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.auth_tokens
    
    def create_auth_token(self, token_data: Dict[str, Any]) -> AuthTokenModel:
        """Create a new authentication token"""
        try:
            token = AuthTokenModel(**token_data)
            token.update_timestamp()
            
            result = self.collection.insert_one(token.model_dump(by_alias=True))
            token.id = result.inserted_id
            
            logger.info(f"Created auth token with ID: {token.id}")
            return token
        except Exception as e:
            logger.error(f"Failed to create auth token: {e}")
            raise
    
    def get_token_by_id(self, token_id: str) -> Optional[AuthTokenModel]:
        """Get authentication token by ID"""
        try:
            from bson import ObjectId
            token_doc = self.collection.find_one({"_id": ObjectId(token_id)})
            if token_doc:
                return AuthTokenModel(**token_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get auth token by ID {token_id}: {e}")
            raise
    
    def get_token_by_value(self, token_value: str) -> Optional[AuthTokenModel]:
        """Get authentication token by token value"""
        try:
            token_doc = self.collection.find_one({"token": token_value})
            if token_doc:
                return AuthTokenModel(**token_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get auth token by value: {e}")
            raise
    
    def get_tokens_by_user_id(self, user_id: str) -> List[AuthTokenModel]:
        """Get all tokens for a specific user"""
        try:
            tokens = []
            cursor = self.collection.find({"user_id": user_id})
            for token_doc in cursor:
                tokens.append(AuthTokenModel(**token_doc))
            return tokens
        except Exception as e:
            logger.error(f"Failed to get tokens for user {user_id}: {e}")
            raise
    
    def get_tokens_by_type(self, user_id: str, token_type: str) -> List[AuthTokenModel]:
        """Get tokens of a specific type for a user"""
        try:
            tokens = []
            cursor = self.collection.find({
                "user_id": user_id,
                "token_type": token_type
            })
            for token_doc in cursor:
                tokens.append(AuthTokenModel(**token_doc))
            return tokens
        except Exception as e:
            logger.error(f"Failed to get {token_type} tokens for user {user_id}: {e}")
            raise
    
    def revoke_token(self, token_id: str) -> bool:
        """Revoke a token by setting is_revoked to True"""
        try:
            from bson import ObjectId
            result = self.collection.update_one(
                {"_id": ObjectId(token_id)},
                {"$set": {"is_revoked": True, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to revoke token {token_id}: {e}")
            raise
    
    def revoke_user_tokens(self, user_id: str, token_type: Optional[str] = None) -> bool:
        """Revoke all tokens for a user, optionally filtered by type"""
        try:
            query = {"user_id": user_id}
            if token_type:
                query["token_type"] = token_type
                
            result = self.collection.update_many(
                query,
                {"$set": {"is_revoked": True, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to revoke tokens for user {user_id}: {e}")
            raise
    
    def delete_expired_tokens(self) -> int:
        """Delete all expired tokens"""
        try:
            result = self.collection.delete_many({
                "expires_at": {"$lt": datetime.utcnow()}
            })
            deleted_count = result.deleted_count
            logger.info(f"Deleted {deleted_count} expired tokens")
            return deleted_count
        except Exception as e:
            logger.error(f"Failed to delete expired tokens: {e}")
            raise
    
    def update_token(self, token_id: str, update_data: Dict[str, Any]) -> Optional[AuthTokenModel]:
        """Update token information"""
        try:
            from bson import ObjectId
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(token_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_token_by_id(token_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update token {token_id}: {e}")
            raise
    
    def delete_token(self, token_id: str) -> bool:
        """Delete a token"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(token_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete token {token_id}: {e}")
            raise
