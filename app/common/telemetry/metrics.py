from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from app.config.config import get_settings

########################################################################

settings = get_settings()
service_identifier = settings.SERVICE_IDENTIFIER

meter_name = f"{service_identifier}-meter"
resource = Resource(attributes={SERVICE_NAME: service_identifier})

metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
metrics_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(metrics_provider)
meter = metrics.get_meter(meter_name)

