from fastapi import HTTPException
from app.domain_types.miscellaneous.exceptions import (
    HTTPError, NotFound, Unauthorized, Forbidden, Conflict, 
    ValidationError, UUIDValidationError
)
from app.common.logger import logger


def handle_service_exception(e: Exception, operation: str = "operation") -> HTTPException:
    """
    Convert service layer exceptions to proper HTTPExceptions with consistent error handling
    
    Args:
        e: The exception to handle
        operation: Description of the operation being performed (for logging)
    
    Returns:
        HTTPException with appropriate status code and message
    """
    
    if isinstance(e, UUIDValidationError):
        logger.error(f"UUID validation error during {operation}: {e.message}")
        return HTTPException(status_code=422, detail=e.message)
    
    elif isinstance(e, NotFound):
        logger.error(f"Resource not found during {operation}: {e.message}")
        return HTTPException(status_code=404, detail=e.message)
    
    elif isinstance(e, Unauthorized):
        logger.error(f"Unauthorized access during {operation}: {e.message}")
        return HTTPException(status_code=401, detail=e.message)
    
    elif isinstance(e, Forbidden):
        logger.error(f"Forbidden access during {operation}: {e.message}")
        return HTTPException(status_code=403, detail=e.message)
    
    elif isinstance(e, Conflict):
        logger.error(f"Conflict error during {operation}: {e.message}")
        return HTTPException(status_code=409, detail=e.message)
    
    elif isinstance(e, ValidationError):
        logger.error(f"Validation error during {operation}: {e.message}")
        return HTTPException(status_code=422, detail=e.message)
    
    elif isinstance(e, HTTPError):
        logger.error(f"HTTP error during {operation}: {e.message}")
        return HTTPException(status_code=e.status_code, detail=e.message)
    
    elif isinstance(e, HTTPException):
        logger.error(f"HTTP exception during {operation}: {e.detail}")
        return e
    
    else:
        # Generic exception handling
        logger.error(f"Unexpected error during {operation}: {str(e)}")
        return HTTPException(status_code=500, detail=f"Internal server error during {operation}")


def log_and_raise_http_exception(
    status_code: int, 
    detail: str, 
    operation: str = "operation"
) -> HTTPException:
    """
    Create and log an HTTPException
    
    Args:
        status_code: HTTP status code
        detail: Error message
        operation: Description of the operation being performed
        
    Returns:
        HTTPException
    """
    logger.error(f"Error during {operation}: {detail}")
    return HTTPException(status_code=status_code, detail=detail)


def safe_execute_service_operation(operation_func, operation_name: str, db_session=None):
    """
    Safely execute a service operation with proper error handling
    
    Args:
        operation_func: Function to execute
        operation_name: Name of the operation for logging
        db_session: Database session (will be rolled back on error)
        
    Returns:
        Result of operation_func or raises HTTPException
    """
    try:
        return operation_func()
    except Exception as e:
        if db_session:
            db_session.rollback()
        raise handle_service_exception(e, operation_name)
