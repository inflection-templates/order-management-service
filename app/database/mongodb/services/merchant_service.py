from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.merchant import MerchantModel
from app.domain_types.schemas.merchant import MerchantCreateModel, MerchantUpdateModel, MerchantSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBMerchantService:
    """MongoDB merchant service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.merchants
    
    def create_merchant(self, model: MerchantCreateModel) -> MerchantModel:
        """Create a new merchant"""
        try:
            merchant_dict = model.model_dump()
            merchant = MerchantModel(**merchant_dict)
            merchant.update_timestamp()
            
            result = self.collection.insert_one(merchant.model_dump(by_alias=True))
            merchant.id = result.inserted_id
            
            logger.info(f"Created merchant with ID: {merchant.id}")
            return merchant.__dict__
        except Exception as e:
            logger.error(f"Failed to create merchant: {e}")
            raise
    
    def get_merchant_by_id(self, merchant_id: str) -> Optional[MerchantModel]:
        """Get merchant by ID"""
        try:
            from bson import ObjectId
            merchant_doc = self.collection.find_one({"_id": ObjectId(merchant_id)})
            if merchant_doc:
                return MerchantModel(**merchant_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get merchant by ID {merchant_id}: {e}")
            raise
    
    def update_merchant(self, merchant_id: str, model: MerchantUpdateModel) -> Optional[MerchantModel]:
        """Update merchant"""
        try:
            from bson import ObjectId
            update_data = model.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(merchant_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_merchant_by_id(merchant_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update merchant {merchant_id}: {e}")
            raise
    
    def delete_merchant(self, merchant_id: str) -> bool:
        """Delete merchant"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(merchant_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete merchant {merchant_id}: {e}")
            raise
    
    def search_merchants(self, search_filter: MerchantSearchFilter) -> List[MerchantModel]:
        """Search merchants with filters"""
        try:
            query = {}
            
            if search_filter.Name:
                query["Name"] = {"$regex": search_filter.Name, "$options": "i"}
            
            if search_filter.IsActive is not None:
                query["IsActive"] = search_filter.IsActive
            
            cursor = self.collection.find(query)
            merchants = [MerchantModel(**merchant_doc) for merchant_doc in cursor]
            
            return merchants
        except Exception as e:
            logger.error(f"Failed to search merchants: {e}")
            raise