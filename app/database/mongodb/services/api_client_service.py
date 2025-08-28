from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.api_client import ApiClientModel
from app.domain_types.schemas.api_client import ApiClientCreateModel, ApiClientUpdateModel, ApiClientSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBApiClientService:
    """MongoDB API client service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.api_clients
    
    def create_api_client(self, model: ApiClientCreateModel) -> ApiClientModel:
        """Create a new API client"""
        try:
            api_client_dict = model.model_dump()
            api_client = ApiClientModel(**api_client_dict)
            api_client.update_timestamp()
            
            result = self.collection.insert_one(api_client.model_dump(by_alias=True))
            api_client.id = result.inserted_id
            
            logger.info(f"Created API client with ID: {api_client.id}")
            return api_client.__dict__
        except Exception as e:
            logger.error(f"Failed to create API client: {e}")
            raise
    
    def get_api_client_by_id(self, api_client_id: str) -> Optional[ApiClientModel]:
        """Get API client by ID"""
        try:
            from bson import ObjectId
            api_client_doc = self.collection.find_one({"_id": ObjectId(api_client_id)})
            if api_client_doc:
                return ApiClientModel(**api_client_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get API client by ID {api_client_id}: {e}")
            raise
    
    def update_api_client(self, api_client_id: str, model: ApiClientUpdateModel) -> Optional[ApiClientModel]:
        """Update API client"""
        try:
            from bson import ObjectId
            update_data = model.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(api_client_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_api_client_by_id(api_client_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update API client {api_client_id}: {e}")
            raise
    
    def delete_api_client(self, api_client_id: str) -> bool:
        """Delete API client"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(api_client_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete API client {api_client_id}: {e}")
            raise
    
    def search_api_clients(self, search_filter: ApiClientSearchFilter) -> List[ApiClientModel]:
        """Search API clients with filters"""
        try:
            query = {}
            
            if search_filter.Name:
                query["Name"] = {"$regex": search_filter.Name, "$options": "i"}
            
            if search_filter.IsActive is not None:
                query["IsActive"] = search_filter.IsActive
            
            cursor = self.collection.find(query)
            api_clients = [ApiClientModel(**api_client_doc) for api_client_doc in cursor]
            
            return api_clients
        except Exception as e:
            logger.error(f"Failed to search API clients: {e}")
            raise