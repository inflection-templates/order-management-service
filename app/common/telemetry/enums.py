
from enum import Enum

class TracingExporterType(str, Enum):
    ZipkinJson       = 'ZipkinJson'
    ZipkinProtobuf   = 'ZipkinProtobuf'
    JaegerThrift     = 'JaegerThrift'
    JaegerProtobuf   = 'JaegerProtobuf'
    Otlp             = 'Otlp'
    Console          = 'Console'
    NoExporter       = 'NoExporter'

def get_tracing_exporter_type(exporter: str):
    if exporter.lower() == "ZipkinJson".lower():
        return TracingExporterType.ZipkinJson
    elif exporter.lower() == "ZipkinProtobuf".lower():
        return TracingExporterType.ZipkinProtobuf
    elif exporter.lower() == "JaegerThrift".lower():
        return TracingExporterType.JaegerThrift
    elif exporter.lower() == "JaegerProtobuf".lower():
        return TracingExporterType.JaegerProtobuf
    elif exporter.lower() == "Otlp".lower():
        return TracingExporterType.Otlp
    elif exporter.lower() == "Console".lower():
        return TracingExporterType.Console
    else:
        return None
