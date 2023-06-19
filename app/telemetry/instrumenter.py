from starlette.requests import Headers
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from fastapi import FastAPI, Request
from app.startup.application import app
# from .metrics import meter_provider
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry import trace
from .tracing import (
    inject_headers,
    tracer_provider,
    extract_context_from_headers,
    tracing_enabled,
    tracer
)

#################################################################

# Instrument the FastAPI app

def instrument():
    
    # This has to be comma separated list...
    excluded_paths = "/health-check,/,/docs"    # Health check, service root, and swagger UI endpoints

    FastAPIInstrumentor.instrument_app(
        app, 
        excluded_urls=excluded_paths, 
        tracer_provider=tracer_provider,
        # meter_provider=meter_provider
    )

#################################################################

# Add a middleware to add a tracing header to all requests

@app.middleware("http")
async def add_tracing_header(request: Request, call_next):

    if tracing_enabled:

        parent_context = trace.get_current_span().get_span_context()
        route_path = request.url.path
        method = request.method
        headers: Headers = request.headers
        span_name = f"Request->{method}:{route_path}"
        context = extract_context_from_headers(headers)
        if context is None:
            context = parent_context

        with tracer.start_as_current_span(span_name, context=context) as current_span:

            # Add the route path and method as attributes to the span

            current_span.set_attribute(SpanAttributes.HTTP_METHOD, method)
            current_span.set_attribute(SpanAttributes.HTTP_ROUTE, route_path)

            # Call the next middleware in pipeline
            response = await call_next(request)

            # Add the trace_id to the response header
            trace_id = trace.get_current_span().get_span_context().trace_id
            response.headers["trace_id"] = str(trace_id)
            inject_headers(response.headers)

            return response
    else:
        # Call the next middleware in pipeline
        response = await call_next(request)
        return response
