from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from app.telemetry.exporters import get_tracing_exporter
from app.config.config import get_settings
from app.telemetry.enums import (
    get_tracing_exporter_type, 
    TracingExporterType
)

########################################################################

settings = get_settings()
service_identifier = settings.SERVICE_IDENTIFIER

########################################################################

# Tracing

tracer_name = f"{service_identifier}-tracer"

resource = Resource(attributes={SERVICE_NAME: service_identifier})
tracer_provider = TracerProvider(resource = resource)
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(tracer_name)
# Exporter and span processor
exporter_type = get_tracing_exporter_type(settings.TRACING_EXPORTER_TYPE)
if exporter_type != None and exporter_type.lower() != TracingExporterType.NoExporter.value.lower():
    exporter = get_tracing_exporter(exporter_type, settings.TRACING_COLLECTOR_ENDPOINT)
    span_processor = BatchSpanProcessor(exporter)
    tracer_provider.add_span_processor(span_processor)

########################################################################

def tracing_enabled():
    if exporter_type == None:
        return False
    elif exporter_type.lower() == TracingExporterType.NoExporter.value.lower():
        return False
    elif settings.TRACING_ENABLED == False:
        return False
    return True
