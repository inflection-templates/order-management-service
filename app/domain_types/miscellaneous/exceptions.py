from starlette.exceptions import HTTPException

class HTTPError(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)
        self.status_code = status_code
        self.message = message

class InvalidUsage(HTTPError):
    def __init__(self, message: str):
        super().__init__(status_code=400, message=message)

class Unauthorized(HTTPError):
    def __init__(self, message: str):
        super().__init__(status_code=401, message=message)

class Forbidden(HTTPError):
    def __init__(self, message: str):
        super().__init__(status_code=403, message=message)

class NotFound(HTTPError):
    def __init__(self, message: str):
        super().__init__(status_code=404, message=message)

class MethodNotAllowed(HTTPError):
    def __init__(self, message: str):
        super().__init__(status_code=405, message=message)

class NotAcceptable(HTTPError):
    def __init__(self, message: str):
        super().__init__(status_code=406, message=message)

class RequestTimeout(HTTPError):
    def __init__(self, message: str):
        super().__init__(status_code=408, message=message)

class Conflict(HTTPError):
    def __init__(self, message: str):
        super().__init__(status_code=409, message=message)

class Gone(HTTPError):
    def __init__(self, message: str):
        super().__init__(status_code=410, message=message)

class ValidationError(HTTPError):
    def __init__(self, message: str):
        super().__init__(status_code=422, message=message)

class UUIDValidationError(HTTPError):
    def __init__(self, message: str = "Provided id is not a valid UUID."):
        super().__init__(status_code=422, message=message)
