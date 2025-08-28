from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.coupon import CouponModel
from app.domain_types.schemas.coupon import CouponCreateModel, CouponUpdateModel, CouponSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBCouponService:
    """MongoDB coupon service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.coupons
    
    def create_coupon(self, model: CouponCreateModel) -> CouponModel:
        """Create a new coupon"""
        try:
            coupon_dict = model.model_dump()
            coupon = CouponModel(**coupon_dict)
            coupon.update_timestamp()
            
            result = self.collection.insert_one(coupon.model_dump(by_alias=True))
            coupon.id = result.inserted_id
            
            logger.info(f"Created coupon with ID: {coupon.id}")
            return coupon.__dict__
        except Exception as e:
            logger.error(f"Failed to create coupon: {e}")
            raise
    
    def get_coupon_by_id(self, coupon_id: str) -> Optional[CouponModel]:
        """Get coupon by ID"""
        try:
            from bson import ObjectId
            coupon_doc = self.collection.find_one({"_id": ObjectId(coupon_id)})
            if coupon_doc:
                return CouponModel(**coupon_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get coupon by ID {coupon_id}: {e}")
            raise
    
    def update_coupon(self, coupon_id: str, model: CouponUpdateModel) -> Optional[CouponModel]:
        """Update coupon"""
        try:
            from bson import ObjectId
            update_data = model.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(coupon_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_coupon_by_id(coupon_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update coupon {coupon_id}: {e}")
            raise
    
    def delete_coupon(self, coupon_id: str) -> bool:
        """Delete coupon"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(coupon_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete coupon {coupon_id}: {e}")
            raise
    
    def search_coupons(self, search_filter: CouponSearchFilter) -> List[CouponModel]:
        """Search coupons with filters"""
        try:
            query = {}
            
            if search_filter.Code:
                query["Code"] = {"$regex": search_filter.Code, "$options": "i"}
            
            if search_filter.IsActive is not None:
                query["IsActive"] = search_filter.IsActive
            
            cursor = self.collection.find(query)
            coupons = [CouponModel(**coupon_doc) for coupon_doc in cursor]
            
            return coupons
        except Exception as e:
            logger.error(f"Failed to search coupons: {e}")
            raise