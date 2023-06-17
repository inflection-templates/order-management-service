from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi import FastAPI
from .tracing import tracer_provider
# from .metrics import meter_provider

def instrument(app: FastAPI):
   
    excluded_paths = [
        "/health-check",    # Health check endpoint
        "/"                 # Service root endpoint
        "/docs"             # Swagger UI endpoint
        ]
    
    FastAPIInstrumentor.instrument_app(
        app, 
        excluded_urls=excluded_paths, 
        tracer_provider=tracer_provider,
        # meter_provider=meter_provider
    )
