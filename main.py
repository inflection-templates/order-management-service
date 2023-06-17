from fastapi import Request, status
import uvicorn
from app.common.logger import logger
from app.startup.application import get_application

# Exception Handling imports
from app.domain_types.miscellaneous.exceptions import HTTPError
from app.config.constants import PORT
from app.config.config import get_settings
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError

# Telemetry imports
from app.telemetry.tracing import (
    tracing_enabled,
    tracer
)
from opentelemetry import trace
from app.telemetry.instrumenter import instrument

#################################################################

app = get_application()

#################################################################

# Exception Handlers

# Predefined Commonly raised HTTP Errors

@app.exception_handler(HTTPError)
async def api_error_handler(request: Request, exc: HTTPError):

    # Handle telemetry and logging here...
    logger.error(f"API Error: {exc.message}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "Message": exc.message,
            "Status": "Failure",
            "Data" : None
        },
    )

# Validation Errors

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    # Handle telemetry and logging here...
    logger.error(f"Validation Error: {exc.errors()}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "Message": "Validation Error",
                "Status": "Failure",
                "Errors": exc.errors(), 
                "RequestBody": exc.body
            }
        ),
    )

# Database Errors

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    # Handle telemetry and logging here...
    logger.error(f"Database Error: {exc.args}")

    # Return a generic error message to the client
    # Do not return the actual error message to the client
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {
                "Message": "Database Error",
                "Status": "Failure",
                "Errors": exc.args,
            }
        ),
    )

# Generic Errors

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Handle telemetry and logging here...
    logger.error(f"Internal Server Error: {exc.args}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {
                "Message": "Internal Server Error",
                "Status": "Failure",
                "Errors": exc.args,
            }
        ),
    )

#################################################################

# Telemetry

tracing = tracing_enabled()
if tracing:
    instrument(app)

# Add a middleware to add a tracing header to all requests
@app.middleware("http")
async def add_tracing_header(request: Request, call_next):
    if tracing:
        with tracer.start_as_current_span("Request"):
            response = await call_next(request)
            trace_id = trace.get_current_span().get_span_context().trace_id
            response.headers["trace_id"] = str(trace_id)
            return response
    else:
        response = await call_next(request)
        return response

#################################################################

# Run the application server

if __name__ == "__main__":
    settings = get_settings()
    if settings.ENVIRONMENT == "development":
        logger.info("Running in development mode")
        uvicorn.run(app, host="localhost", port=PORT)
    else:
        logger.info("Running in production mode")
        uvicorn.run(app, host="0.0.0.0", port=PORT)
