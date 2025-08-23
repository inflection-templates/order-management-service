from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.customer import CustomerModel
from app.domain_types.schemas.customer import CustomerCreateModel, CustomerUpdateModel, CustomerSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBCustomerService:
    """MongoDB customer service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.customers
    
    def create_customer(self, customer_data: CustomerCreateModel) -> CustomerModel:
        """Create a new customer"""
        try:
            customer_dict = customer_data.dict()
            customer = CustomerModel(**customer_dict)
            customer.update_timestamp()
            
            result = self.collection.insert_one(customer.dict(by_alias=True))
            customer.id = result.inserted_id
            
            logger.info(f"Created customer with ID: {customer.id}")
            return customer
        except Exception as e:
            logger.error(f"Failed to create customer: {e}")
            raise
    
    def get_customer_by_id(self, customer_id: str) -> Optional[CustomerModel]:
        """Get customer by ID"""
        try:
            from bson import ObjectId
            customer_doc = self.collection.find_one({"_id": ObjectId(customer_id)})
            if customer_doc:
                return CustomerModel(**customer_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get customer by ID {customer_id}: {e}")
            raise
    
    def update_customer(self, customer_id: str, customer_data: CustomerUpdateModel) -> Optional[CustomerModel]:
        """Update customer"""
        try:
            from bson import ObjectId
            update_data = customer_data.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(customer_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_customer_by_id(customer_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update customer {customer_id}: {e}")
            raise
    
    def delete_customer(self, customer_id: str) -> bool:
        """Delete customer"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(customer_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete customer {customer_id}: {e}")
            raise
    
    def search_customers(self, search_filter: CustomerSearchFilter) -> List[CustomerModel]:
        """Search customers with filters"""
        try:
            query = {}
            
            if search_filter.email:
                query["email"] = {"$regex": search_filter.email, "$options": "i"}
            
            if search_filter.is_active is not None:
                query["is_active"] = search_filter.is_active
            
            cursor = self.collection.find(query)
            customers = [CustomerModel(**customer_doc) for customer_doc in cursor]
            
            return customers
        except Exception as e:
            logger.error(f"Failed to search customers: {e}")
            raise

