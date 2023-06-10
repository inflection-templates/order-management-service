
from starlette.exceptions import HTTPException

class CustomException(HTTPException):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

class InvalidUsage(CustomException):
    def __init__(self, message: str):
        self.status_code = 400
        self.message = message

class Unauthorized(CustomException):
    def __init__(self, message: str):
        self.status_code = 401
        self.message = message

class Forbidden(CustomException):
    def __init__(self, message: str):
        self.status_code = 403
        self.message = message

class NotFound(CustomException):
    def __init__(self, message: str):
        self.status_code = 404
        self.message = message

class MethodNotAllowed(CustomException):
    def __init__(self, message: str):
        self.status_code = 405
        self.message = message

class NotAcceptable(CustomException):
    def __init__(self, message: str):
        self.status_code = 406
        self.message = message

class RequestTimeout(CustomException):
    def __init__(self, message: str):
        self.status_code = 408
        self.message = message

class Conflict(CustomException):
    def __init__(self, message: str):
        self.status_code = 409
        self.message = message

class Gone(CustomException):
    def __init__(self, message: str):
        self.status_code = 410
        self.message = message

class ValidationError(CustomException):
    def __init__(self, message: str):
        self.status_code = 422
        self.message = message

class UUIDValidationError(CustomException):
    def __init__(self, message: str = "Provided id is not a valid UUID."):
        self.status_code = 422
        self.message = message
