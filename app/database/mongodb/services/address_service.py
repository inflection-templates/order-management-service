from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.address import AddressModel
from app.domain_types.schemas.address import AddressCreateModel, AddressUpdateModel, AddressSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBAddressService:
    """MongoDB address service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.addresses
    
    def create_address(self, address_data: AddressCreateModel) -> AddressModel:
        """Create a new address"""
        try:
            address_dict = address_data.dict()
            address = AddressModel(**address_dict)
            address.update_timestamp()
            
            result = self.collection.insert_one(address.dict(by_alias=True))
            address.id = result.inserted_id
            
            logger.info(f"Created address with ID: {address.id}")
            return address
        except Exception as e:
            logger.error(f"Failed to create address: {e}")
            raise
    
    def get_address_by_id(self, address_id: str) -> Optional[AddressModel]:
        """Get address by ID"""
        try:
            from bson import ObjectId
            address_doc = self.collection.find_one({"_id": ObjectId(address_id)})
            if address_doc:
                return AddressModel(**address_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get address by ID {address_id}: {e}")
            raise
    
    def update_address(self, address_id: str, address_data: AddressUpdateModel) -> Optional[AddressModel]:
        """Update address"""
        try:
            from bson import ObjectId
            update_data = address_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(address_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_address_by_id(address_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update address {address_id}: {e}")
            raise
    
    def delete_address(self, address_id: str) -> bool:
        """Delete address"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(address_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete address {address_id}: {e}")
            raise
    
    def search_addresses(self, search_filter: AddressSearchFilter) -> List[AddressModel]:
        """Search addresses with filters"""
        try:
            query = {}
            
            if search_filter.CustomerId:
                query["CustomerId"] = search_filter.CustomerId
            
            if search_filter.City:
                query["City"] = {"$regex": search_filter.City, "$options": "i"}
            
            cursor = self.collection.find(query)
            addresses = [AddressModel(**address_doc) for address_doc in cursor]
            
            return addresses
        except Exception as e:
            logger.error(f"Failed to search addresses: {e}")
            raise