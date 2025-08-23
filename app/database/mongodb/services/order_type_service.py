from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.order_type import OrderTypeModel
from app.domain_types.schemas.order_type import OrderTypeCreateModel, OrderTypeUpdateModel, OrderTypeSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBOrderTypeService:
    """MongoDB order type service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.order_types
    
    def create_order_type(self, order_type_data: OrderTypeCreateModel) -> OrderTypeModel:
        """Create a new order type"""
        try:
            order_type_dict = order_type_data.dict()
            order_type = OrderTypeModel(**order_type_dict)
            order_type.update_timestamp()
            
            result = self.collection.insert_one(order_type.dict(by_alias=True))
            order_type.id = result.inserted_id
            
            logger.info(f"Created order type with ID: {order_type.id}")
            return order_type
        except Exception as e:
            logger.error(f"Failed to create order type: {e}")
            raise
    
    def get_order_type_by_id(self, order_type_id: str) -> Optional[OrderTypeModel]:
        """Get order type by ID"""
        try:
            from bson import ObjectId
            order_type_doc = self.collection.find_one({"_id": ObjectId(order_type_id)})
            if order_type_doc:
                return OrderTypeModel(**order_type_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get order type by ID {order_type_id}: {e}")
            raise
    
    def update_order_type(self, order_type_id: str, order_type_data: OrderTypeUpdateModel) -> Optional[OrderTypeModel]:
        """Update order type"""
        try:
            from bson import ObjectId
            update_data = order_type_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(order_type_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_order_type_by_id(order_type_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update order type {order_type_id}: {e}")
            raise
    
    def delete_order_type(self, order_type_id: str) -> bool:
        """Delete order type"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(order_type_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete order type {order_type_id}: {e}")
            raise
    
    def search_order_types(self, search_filter: OrderTypeSearchFilter) -> List[OrderTypeModel]:
        """Search order types with filters"""
        try:
            query = {}
            
            if search_filter.Name:
                query["Name"] = {"$regex": search_filter.Name, "$options": "i"}
            
            if search_filter.IsActive is not None:
                query["IsActive"] = search_filter.IsActive
            
            cursor = self.collection.find(query)
            order_types = [OrderTypeModel(**order_type_doc) for order_type_doc in cursor]
            
            return order_types
        except Exception as e:
            logger.error(f"Failed to search order types: {e}")
            raise