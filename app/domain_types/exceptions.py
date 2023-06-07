
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
