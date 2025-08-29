from pymongo import MongoClient
from pymongo.database import Database
from app.config.config import get_settings
from app.common.logger import logger

# Global flag to prevent multiple initializations
_database_initialized = False

class MongoDBInitializer:
    """MongoDB database initializer"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client: MongoClient = None
        self.database: Database = None
    
    def initialize_database(self) -> bool:
        """Initialize MongoDB connection and database"""
        global _database_initialized
        
        if _database_initialized:
            print("[MongoDB] Database already initialized, skipping...")
            return True
            
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
            
            # Check if database exists
            database_names = self.client.list_database_names()
            database_exists = self.settings.MONGODB_DATABASE in database_names
            
            if not database_exists:
                # Database doesn't exist, it will be created when first collection is created
                print(f"[MongoDB] Database '{self.settings.MONGODB_DATABASE}' not found")
            else:
                print(f"[MongoDB] Database '{self.settings.MONGODB_DATABASE}' already exists")
            
            # Get database
            self.database = self.client[self.settings.MONGODB_DATABASE]
            
            # Create collections if they don't exist
            self._create_collections()
            
            # Show appropriate success message based on whether database existed
            if database_exists:
                print(f"[MongoDB] Connected to database: '{self.settings.MONGODB_DATABASE}'")
            else:
                print(f"[MongoDB] Creating database: '{self.settings.MONGODB_DATABASE}'")
            
            _database_initialized = True
            return True
            
        except Exception as e:
            print(f"[MongoDB] Failed to initialize MongoDB: {e}")
            return False
    
    def _create_collections(self):
        """Create MongoDB collections if they don't exist"""
        collections = [
            "users", "orders", "customers", "merchants", "carts", 
            "coupons", "payment_transactions", "order_line_items",
            "order_history", "order_types", "addresses", "roles", "api_clients",
            "auth_tokens", "tenants", "user_roles", "user_external_auths", "user_login_sessions"
        ]
        
        for collection_name in collections:
            if collection_name not in self.database.list_collection_names():
                # Collection doesn't exist, create it silently
                self.database.create_collection(collection_name)
                # Removed all print statements for collection creation
    
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

def test_database_connection() -> bool:
    """
    Test connection to the specific database.
    Returns True if successful, False otherwise.
    """
    try:
        # Test connection to the specific database
        client = MongoClient(mongodb_initializer.settings.MONGODB_URI)
        
        # Simple test command
        client.admin.command('ping')
        logger.debug(f"[MongoDB] Successfully connected to database '{mongodb_initializer.settings.MONGODB_DATABASE}'")
        client.close()
        return True
                
    except Exception as e:
        logger.error(f"[MongoDB] Failed to connect to database '{mongodb_initializer.settings.MONGODB_DATABASE}': {e}")
        return False

# Global flag for collection creation
_collections_created = False

def create_collections_if_not_exist():
    """
    Create all collections if they don't exist.
    This function creates the MongoDB collections.
    """
    global _collections_created
    
    if _collections_created:        
        return True
    
    try:
        # Initialize database if not already done
        if not _database_initialized:
            initialize_database()
        
        # Create collections
        mongodb_initializer._create_collections()
        
        # logger.info("[MongoDB] Database collections created successfully!")
        _collections_created = True
        return True
        
    except Exception as e:
        logger.error(f"[MongoDB] Failed to create collections: {e}")
        return False
