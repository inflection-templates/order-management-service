from typing import Callable, Any
from app.database.orm_factory import orm_factory

class DatabaseInterface:
    """Unified interface for database operations across ORMs"""
    
    def __init__(self):
        self.orm_factory = orm_factory
        self._service_cache = {}  # Cache imported services
        print(f"Database Interface initialized with {self.orm_factory.orm_type.value.upper()} ORM")
    
    def get_db_session(self):
        """Get database session for the active ORM"""
        return self.orm_factory.get_database_accessor()
    
    def _get_service(self, service_name: str):
        """Get service with caching"""
        if service_name not in self._service_cache:
            self._service_cache[service_name] = self.orm_factory.get_service_module(service_name)
        return self._service_cache[service_name]
    
    def get_order_service(self):
        """Get order service for the active ORM"""
        return self._get_service("order_service")
    
    def get_customer_service(self):
        """Get customer service for the active ORM"""
        return self._get_service("customer_service")
    
    def get_merchant_service(self):
        """Get merchant service for the active ORM"""
        return self._get_service("merchant_service")
    
    def get_cart_service(self):
        """Get cart service for the active ORM"""
        return self._get_service("cart_service")
    
    def get_address_service(self):
        """Get address service for the active ORM"""
        return self._get_service("address_service")
    
    def get_coupon_service(self):
        """Get coupon service for the active ORM"""
        return self._get_service("coupon_service")
    
    def get_payment_transaction_service(self):
        """Get payment transaction service for the active ORM"""
        return self._get_service("payment_transaction_service")
    
    def get_order_line_item_service(self):
        """Get order line item service for the active ORM"""
        return self._get_service("order_line_item_service")
    
    def get_order_history_service(self):
        """Get order history service for the active ORM"""
        return self._get_service("order_history_service")
    
    def get_order_type_service(self):
        """Get order type service for the active ORM"""
        return self._get_service("order_type_service")
    
    def get_user_service(self):
        """Get user service for the active ORM"""
        return self._get_service("user_service")
    
    def get_role_service(self):
        """Get role service for the active ORM"""
        return self._get_service("role_service")
    
    def get_api_client_service(self):
        """Get API client service for the active ORM"""
        return self._get_service("api_client_service")

# Global database interface instance
db_interface = DatabaseInterface()
