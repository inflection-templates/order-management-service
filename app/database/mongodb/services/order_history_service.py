from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.order_history import OrderHistoryModel
from app.domain_types.schemas.order_history import OrderHistoryCreateModel, OrderHistoryUpdateModel, OrderHistorySearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBOrderHistoryService:
    """MongoDB order history service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.order_history
    
    def create_order_history(self, model: OrderHistoryCreateModel) -> OrderHistoryModel:
        """Create a new order history entry"""
        try:
            history_dict = model.model_dump()
            history = OrderHistoryModel(**history_dict)
            history.update_timestamp()
            
            result = self.collection.insert_one(history.model_dump(by_alias=True))
            history.id = result.inserted_id
            
            logger.info(f"Created order history with ID: {history.id}")
            return history.__dict__
        except Exception as e:
            logger.error(f"Failed to create order history: {e}")
            raise
    
    def get_order_history_by_id(self, history_id: str) -> Optional[OrderHistoryModel]:
        """Get order history by ID"""
        try:
            from bson import ObjectId
            history_doc = self.collection.find_one({"_id": ObjectId(history_id)})
            if history_doc:
                return OrderHistoryModel(**history_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get order history by ID {history_id}: {e}")
            raise
    
    def update_order_history(self, history_id: str, model: OrderHistoryUpdateModel) -> Optional[OrderHistoryModel]:
        """Update order history"""
        try:
            from bson import ObjectId
            update_data = model.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(history_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_order_history_by_id(history_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update order history {history_id}: {e}")
            raise
    
    def delete_order_history(self, history_id: str) -> bool:
        """Delete order history"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(history_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete order history {history_id}: {e}")
            raise
    
    def search_order_history(self, search_filter: OrderHistorySearchFilter) -> List[OrderHistoryModel]:
        """Search order history with filters"""
        try:
            query = {}
            
            if search_filter.OrderId:
                query["OrderId"] = search_filter.OrderId
            
            if search_filter.Status:
                query["Status"] = search_filter.Status.value
            
            cursor = self.collection.find(query)
            history_entries = [OrderHistoryModel(**history_doc) for history_doc in cursor]
            
            return history_entries
        except Exception as e:
            logger.error(f"Failed to search order history: {e}")
            raise
