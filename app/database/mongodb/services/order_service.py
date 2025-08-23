from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.order import OrderModel
from app.domain_types.schemas.order import OrderCreateModel, OrderUpdateModel, OrderSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBOrderService:
    """MongoDB order service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.orders
    
    def create_order(self, order_data: OrderCreateModel) -> OrderModel:
        """Create a new order"""
        try:
            order_dict = order_data.dict()
            order = OrderModel(**order_dict)
            order.update_timestamp()
            
            result = self.collection.insert_one(order.dict(by_alias=True))
            order.id = result.inserted_id
            
            logger.info(f"Created order with ID: {order.id}")
            return order
        except Exception as e:
            logger.error(f"Failed to create order: {e}")
            raise
    
    def get_order_by_id(self, order_id: str) -> Optional[OrderModel]:
        """Get order by ID"""
        try:
            from bson import ObjectId
            order_doc = self.collection.find_one({"_id": ObjectId(order_id)})
            if order_doc:
                return OrderModel(**order_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get order by ID {order_id}: {e}")
            raise
    
    def update_order(self, order_id: str, order_data: OrderUpdateModel) -> Optional[OrderModel]:
        """Update order"""
        try:
            from bson import ObjectId
            update_data = order_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(order_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_order_by_id(order_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update order {order_id}: {e}")
            raise
    
    def delete_order(self, order_id: str) -> bool:
        """Delete order"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(order_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete order {order_id}: {e}")
            raise
    
    def search_orders(self, search_filter: OrderSearchFilter) -> List[OrderModel]:
        """Search orders with filters"""
        try:
            query = {}
            
            if search_filter.CustomerId:
                query["CustomerId"] = search_filter.CustomerId
            
            if search_filter.OrderStatus:
                query["OrderStatus"] = search_filter.OrderStatus.value
            
            if search_filter.OrderType:
                query["OrderType"] = search_filter.OrderType
            
            cursor = self.collection.find(query)
            orders = [OrderModel(**order_doc) for order_doc in cursor]
            
            return orders
        except Exception as e:
            logger.error(f"Failed to search orders: {e}")
            raise
