from typing import List, Optional, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection
from app.database.mongodb.models.payment_transaction import PaymentTransactionModel
from app.domain_types.schemas.payment_transaction import PaymentTransactionCreateModel, PaymentTransactionResponseModel, PaymentTransactionSearchFilter
from app.common.logger import logger
from datetime import datetime

class MongoDBPaymentTransactionService:
    """MongoDB payment transaction service implementation"""
    
    def __init__(self, db: Database):
        self.db = db
        self.collection: Collection = db.payment_transactions
    
    def create_payment_transaction(self, model: PaymentTransactionCreateModel) -> PaymentTransactionModel:
        """Create a new payment transaction"""
        try:
            transaction_dict = model.model_dump()
            transaction = PaymentTransactionModel(**transaction_dict)
            transaction.update_timestamp()
            
            result = self.collection.insert_one(transaction.model_dump(by_alias=True))
            transaction.id = result.inserted_id
            
            logger.info(f"Created payment transaction with ID: {transaction.id}")
            return transaction.__dict__
        except Exception as e:
            logger.error(f"Failed to create payment transaction: {e}")
            raise
    
    def get_payment_transaction_by_id(self, transaction_id: str) -> Optional[PaymentTransactionModel]:
        """Get payment transaction by ID"""
        try:
            from bson import ObjectId
            transaction_doc = self.collection.find_one({"_id": ObjectId(transaction_id)})
            if transaction_doc:
                return PaymentTransactionModel(**transaction_doc)
            return None
        except Exception as e:
            logger.error(f"Failed to get payment transaction by ID {transaction_id}: {e}")
            raise
    
    def update_payment_transaction(self, transaction_id: str, model: dict) -> Optional[PaymentTransactionModel]:
        """Update payment transaction"""
        try:
            from bson import ObjectId
            update_data = model.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"_id": ObjectId(transaction_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return self.get_payment_transaction_by_id(transaction_id)
            return None
        except Exception as e:
            logger.error(f"Failed to update payment transaction {transaction_id}: {e}")
            raise
    
    def delete_payment_transaction(self, transaction_id: str) -> bool:
        """Delete payment transaction"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({"_id": ObjectId(transaction_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Failed to delete payment transaction {transaction_id}: {e}")
            raise
    
    def search_payment_transactions(self, search_filter: PaymentTransactionSearchFilter) -> List[PaymentTransactionModel]:
        """Search payment transactions with filters"""
        try:
            query = {}
            
            if search_filter.OrderId:
                query["OrderId"] = search_filter.OrderId
            
            if search_filter.PaymentStatus:
                query["PaymentStatus"] = search_filter.PaymentStatus.value
            
            cursor = self.collection.find(query)
            transactions = [PaymentTransactionModel(**transaction_doc) for transaction_doc in cursor]
            
            return transactions
        except Exception as e:
            logger.error(f"Failed to search payment transactions: {e}")
            raise