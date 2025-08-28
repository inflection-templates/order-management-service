from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.order_line_item import OrderLineItemModel
from app.domain_types.schemas.order_line_item import OrderLineItemCreateModel, OrderLineItemUpdateModel, OrderLineItemSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBOrderLineItemService:
    """MongoDB order line item service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.order_line_items
    
    def create_order_line_item(self, model: OrderLineItemCreateModel) -> OrderLineItemModel:
        """Create a new order line item"""
        try:
            line_item_dict = model.model_dump()
            line_item = OrderLineItemModel(**line_item_dict)
            line_item.update_timestamp()
            
            result = self.collection.insert_one(line_item.model_dump(by_alias=True))
            line_item.id = result.inserted_id
            
            logger.info(f"Created order line item with ID: {line_item.id}")
            return line_item.__dict__
        except Exception as e:
            logger.error(f"Failed to create order line item: {e}")
            raise
    
    def get_order_line_item_by_id(self, line_item_id: str) -> Optional[OrderLineItemModel]:
        """Get order line item by ID"""
        try:
            from bson import ObjectId
            line_item_doc = self.collection.find_one({"_id": ObjectId(line_item_id)})
            if line_item_doc:
                return OrderLineItemModel(**line_item_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get order line item by ID {line_item_id}: {e}")
            raise
    
    def update_order_line_item(self, line_item_id: str, model: OrderLineItemUpdateModel) -> Optional[OrderLineItemModel]:
        """Update order line item"""
        try:
            from bson import ObjectId
            update_data = model.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(line_item_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_order_line_item_by_id(line_item_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update order line item {line_item_id}: {e}")
            raise
    
    def delete_order_line_item(self, line_item_id: str) -> bool:
        """Delete order line item"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(line_item_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete order line item {line_item_id}: {e}")
            raise
    
    def search_order_line_items(self, search_filter: OrderLineItemSearchFilter) -> List[OrderLineItemModel]:
        """Search order line items with filters"""
        try:
            query = {}
            
            if search_filter.OrderId:
                query["OrderId"] = search_filter.OrderId
            
            if search_filter.ProductId:
                query["ProductId"] = search_filter.ProductId
            
            cursor = self.collection.find(query)
            line_items = [OrderLineItemModel(**line_item_doc) for line_item_doc in cursor]
            
            return line_items
        except Exception as e:
            logger.error(f"Failed to search order line items: {e}")
            raise
