from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi import FastAPI
from .tracing import tracer_provider
# from .metrics import meter_provider

def instrument(app: FastAPI):
    
    # This has to be comma separated list...
    excluded_paths = "/health-check,/,/docs"    # Health check, service root, and swagger UI endpoints

    FastAPIInstrumentor.instrument_app(
        app, 
        excluded_urls=excluded_paths, 
        tracer_provider=tracer_provider,
        # meter_provider=meter_provider
    )
