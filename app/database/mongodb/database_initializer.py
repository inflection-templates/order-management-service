from pymongo import MongoClient
from pymongo.database import Database
from app.config.config import get_settings
from app.common.logger import logger

class MongoDBInitializer:
    """MongoDB database initializer"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client: MongoClient = None
        self.database: Database = None
    
    def initialize_database(self) -> bool:
        """Initialize MongoDB connection and database"""
        try:
            # Create MongoDB client
            self.client = MongoClient(
                self.settings.MONGODB_URI,
                maxPoolSize=self.settings.MONGODB_MAX_POOL_SIZE,
                minPoolSize=self.settings.MONGODB_MIN_POOL_SIZE,
                maxIdleTimeMS=self.settings.MONGODB_MAX_IDLE_TIME_MS,
                connectTimeoutMS=self.settings.MONGODB_CONNECT_TIMEOUT_MS,
                serverSelectionTimeoutMS=self.settings.MONGODB_SERVER_SELECTION_TIMEOUT_MS
            )
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database
            self.database = self.client[self.settings.MONGODB_DATABASE]
            
            # Create collections if they don't exist
            self._create_collections()
            
            logger.info(f"MongoDB initialized successfully: {self.settings.MONGODB_URI}/{self.settings.MONGODB_DATABASE}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB: {e}")
            return False
    
    def _create_collections(self):
        """Create MongoDB collections if they don't exist"""
        collections = [
            "users", "orders", "customers", "merchants", "carts", 
            "coupons", "payment_transactions", "order_line_items",
            "order_history", "order_types", "addresses", "roles", "api_clients"
        ]
        
        for collection_name in collections:
            if collection_name not in self.database.list_collection_names():
                self.database.create_collection(collection_name)
                logger.info(f"Created collection: {collection_name}")
    
    def get_database(self) -> Database:
        """Get MongoDB database instance"""
        return self.database
    
    def get_client(self) -> MongoClient:
        """Get MongoDB client instance"""
        return self.client
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()

# Global MongoDB initializer instance
mongodb_initializer = MongoDBInitializer()

def initialize_database() -> bool:
    """Initialize MongoDB database"""
    return mongodb_initializer.initialize_database()

def get_database() -> Database:
    """Get MongoDB database instance"""
    return mongodb_initializer.get_database()

def get_client() -> MongoClient:
    """Get MongoDB client instance"""
    return mongodb_initializer.get_client()
