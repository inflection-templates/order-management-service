from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.user_login_session import UserLoginSessionModel
from app.common.logger import logger
from datetime import datetime, date

class MongoDBUserLoginSessionService:
    """MongoDB user login session service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.user_login_sessions
    
    def create_login_session(self, model: Dict[str, Any]) -> UserLoginSessionModel:
        """Create a new user login session"""
        try:
            session = UserLoginSessionModel(**model)
            session.update_timestamp()
            
            result = self.collection.insert_one(session.model_dump(by_alias=True))
            session.id = result.inserted_id
            
            logger.info(f"Created login session with ID: {session.id}")
            return session.__dict__
        except Exception as e:
            logger.error(f"Failed to create login session: {e}")
            raise
    
    def get_session_by_id(self, session_id: str) -> Optional[UserLoginSessionModel]:
        """Get login session by ID"""
        try:
            from bson import ObjectId
            session_doc = self.collection.find_one({"_id": ObjectId(session_id)})
            if session_doc:
                return UserLoginSessionModel(**session_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get login session by ID {session_id}: {e}")
            raise
    
    def get_active_sessions_by_user_id(self, user_id: str) -> List[UserLoginSessionModel]:
        """Get all active login sessions for a user"""
        try:
            sessions = []
            cursor = self.collection.find({
                "user_id": user_id,
                "is_active": True,
                "deleted_at": None,
                "valid_till": {"$gte": date.today()}
            })
            for session_doc in cursor:
                sessions.append(UserLoginSessionModel(**session_doc))
            return sessions
        except Exception as e:
            logger.error(f"Failed to get active sessions for user {user_id}: {e}")
            raise
    
    def get_all_sessions_by_user_id(self, user_id: str) -> List[UserLoginSessionModel]:
        """Get all login sessions for a user (including inactive and expired)"""
        try:
            sessions = []
            cursor = self.collection.find({
                "user_id": user_id,
                "deleted_at": None
            })
            for session_doc in cursor:
                sessions.append(UserLoginSessionModel(**session_doc))
            return sessions
        except Exception as e:
            logger.error(f"Failed to get all sessions for user {user_id}: {e}")
            raise
    
    def get_expired_sessions(self) -> List[UserLoginSessionModel]:
        """Get all expired login sessions"""
        try:
            sessions = []
            cursor = self.collection.find({
                "valid_till": {"$lt": date.today()},
                "deleted_at": None
            })
            for session_doc in cursor:
                sessions.append(UserLoginSessionModel(**session_doc))
            return sessions
        except Exception as e:
            logger.error(f"Failed to get expired sessions: {e}")
            raise
    
    def get_active_sessions(self) -> List[UserLoginSessionModel]:
        """Get all active login sessions across all users"""
        try:
            sessions = []
            cursor = self.collection.find({
                "is_active": True,
                "deleted_at": None,
                "valid_till": {"$gte": date.today()}
            })
            for session_doc in cursor:
                sessions.append(UserLoginSessionModel(**session_doc))
            return sessions
        except Exception as e:
            logger.error(f"Failed to get all active sessions: {e}")
            raise
    
    def activate_session(self, session_id: str) -> bool:
        """Activate a login session"""
        try:
            from bson import ObjectId
            result = self.collection.update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {"is_active": True, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to activate session {session_id}: {e}")
            raise
    
    def deactivate_session(self, session_id: str) -> bool:
        """Deactivate a login session"""
        try:
            from bson import ObjectId
            result = self.collection.update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to deactivate session {session_id}: {session_id}: {e}")
            raise
    
    def extend_session(self, session_id: str, new_valid_till: date) -> bool:
        """Extend the validity of a login session"""
        try:
            from bson import ObjectId
            result = self.collection.update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {"valid_till": new_valid_till, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to extend session {session_id}: {e}")
            raise
    
    def deactivate_user_sessions(self, user_id: str) -> bool:
        """Deactivate all active sessions for a user"""
        try:
            result = self.collection.update_many(
                {"user_id": user_id, "is_active": True},
                {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to deactivate sessions for user {user_id}: {e}")
            raise
    
    def update_session(self, session_id: str, model: Dict[str, Any]) -> Optional[UserLoginSessionModel]:
        """Update login session information"""
        try:
            from bson import ObjectId
            model["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(session_id)},
                {"$set": model}
            )
            
            if result.modified_count > 0:
                return self.get_session_by_id(session_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update session {session_id}: {e}")
            raise
    
    def delete_session(self, session_id: str) -> bool:
        """Hard delete a login session"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(session_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}")
            raise
    
    def soft_delete_session(self, session_id: str) -> bool:
        """Soft delete a login session"""
        try:
            from bson import ObjectId
            result = self.collection.update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {"deleted_at": datetime.utcnow(), "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to soft delete session {session_id}: {e}")
            raise
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions by soft deleting them"""
        try:
            result = self.collection.update_many(
                {
                    "valid_till": {"$lt": date.today()},
                    "deleted_at": None
                },
                {"$set": {"deleted_at": datetime.utcnow(), "updated_at": datetime.utcnow()}}
            )
            updated_count = result.modified_count
            logger.info(f"Cleaned up {updated_count} expired sessions")
            return updated_count
        except Exception as e:
            logger.error(f"Failed to cleanup expired sessions: {e}")
            raise
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """Get statistics about login sessions"""
        try:
            total_sessions = self.collection.count_documents({"deleted_at": None})
            active_sessions = self.collection.count_documents({
                "is_active": True,
                "deleted_at": None,
                "valid_till": {"$gte": date.today()}
            })
            expired_sessions = self.collection.count_documents({
                "valid_till": {"$lt": date.today()},
                "deleted_at": None
            })
            
            return {
                "total_sessions": total_sessions,
                "active_sessions": active_sessions,
                "expired_sessions": expired_sessions
            }
        except Exception as e:
            logger.error(f"Failed to get session statistics: {e}")
            raise
