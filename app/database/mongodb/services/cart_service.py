from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.cart import CartModel
from app.domain_types.schemas.cart import CartCreateModel, CartUpdateModel, CartSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBCartService:
    """MongoDB cart service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.carts
    
    def create_cart(self, model: CartCreateModel) -> CartModel:
        """Create a new cart"""
        try:
            cart_dict = model.model_dump()
            cart = CartModel(**cart_dict)
            cart.update_timestamp()
            
            result = self.collection.insert_one(cart.model_dump(by_alias=True))
            cart.id = result.inserted_id
            
            logger.info(f"Created cart with ID: {cart.id}")
            return cart.__dict__
        except Exception as e:
            logger.error(f"Failed to create cart: {e}")
            raise
    
    def get_cart_by_id(self, cart_id: str) -> Optional[CartModel]:
        """Get cart by ID"""
        try:
            from bson import ObjectId
            cart_doc = self.collection.find_one({"_id": ObjectId(cart_id)})
            if cart_doc:
                return CartModel(**cart_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get cart by ID {cart_id}: {e}")
            raise
    
    def update_cart(self, cart_id: str, model: CartUpdateModel) -> Optional[CartModel]:
        """Update cart"""
        try:
            from bson import ObjectId
            update_data = model.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(cart_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_cart_by_id(cart_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update cart {cart_id}: {e}")
            raise
    
    def delete_cart(self, cart_id: str) -> bool:
        """Delete cart"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(cart_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete cart {cart_id}: {e}")
            raise
    
    def search_carts(self, search_filter: CartSearchFilter) -> List[CartModel]:
        """Search carts with filters"""
        try:
            query = {}
            
            if search_filter.CustomerId:
                query["CustomerId"] = search_filter.CustomerId
            
            if search_filter.IsActive is not None:
                query["IsActive"] = search_filter.IsActive
            
            cursor = self.collection.find(query)
            carts = [CartModel(**cart_doc) for cart_doc in cursor]
            
            return carts
        except Exception as e:
            logger.error(f"Failed to search carts: {e}")
            raise
