import functools
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import SpanKind
from app.telemetry.exporters import get_tracing_exporter, get_tracing_exporter_type
from app.config.config import get_settings
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from fastapi import Request

########################################################################

settings = get_settings()
service_identifier = settings.SERVICE_IDENTIFIER
tracing_enabled = settings.TRACING_ENABLED

########################################################################

# Tracing

tracer = None
tracer_provider = None
resource = None

if tracing_enabled:
    tracer_name = f"{service_identifier}-tracer"
    resource = Resource(attributes={SERVICE_NAME: service_identifier})
    tracer_provider = TracerProvider(resource = resource)
    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer(tracer_name)
    # Exporter and span processor
    exporter_type = get_tracing_exporter_type(settings.TRACING_EXPORTER_TYPE)
    if exporter_type != None:
        exporter = get_tracing_exporter(exporter_type, settings.TRACING_COLLECTOR_ENDPOINT)
        span_processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(span_processor)

########################################################################

# Decorator to trace a function
def trace_span(operation_name, span_kind=SpanKind.INTERNAL):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not tracing_enabled:
                return func(*args, **kwargs)
            else:
                with tracer.start_as_current_span(operation_name, kind=span_kind):
                    return func(*args, **kwargs)
        return wrapper
    return decorator

# Function to inject headers into outgoing requests
# NOTE: This method needs to be fixed
def inject_headers(headers: Request.headers, attributes: dict=None):
    span = trace.get_current_span()
    if attributes != None:
        for key, value in attributes.items():
            span.set_attribute(key, value)
    # Propagate the tracing ID in the outgoing requests
    carrier = {}
    TraceContextTextMapPropagator().inject(carrier)
    header = {"traceparent": carrier["traceparent"]}
    headers.update(header)
    return headers

# Function to extract headers from incoming requests
def extract_context_from_headers(headers):
    # Extract the tracing ID from the incoming requests
    context = TraceContextTextMapPropagator().extract(carrier=headers)
    return context
