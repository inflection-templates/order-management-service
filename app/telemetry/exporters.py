from enum import Enum

#################################################################

class TracingExporterType(str, Enum):
    ZipkinJson       = 'ZipkinJson'
    ZipkinProtobuf   = 'ZipkinProtobuf'
    JaegerThrift     = 'JaegerThrift'
    JaegerProtobuf   = 'JaegerProtobuf'
    Otlp             = 'Otlp'
    Console          = 'Console'

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
        return TracingExporterType.Console

#################################################################

def get_tracing_exporter(
        exporter: TracingExporterType, 
        collector_endpoint: str = None, 
        agent_host: str = None, 
        agent_port: int = None):
    if exporter == TracingExporterType.ZipkinJson:
        return get_zipkin_exporter_json(collector_endpoint)
    elif exporter == TracingExporterType.ZipkinProtobuf:
        return get_zipkin_exporter_protobuf(collector_endpoint)
    elif exporter == TracingExporterType.JaegerThrift:
        return get_jaeger_exporter_thrift(agent_host, agent_port, collector_endpoint)
    elif exporter == TracingExporterType.JaegerProtobuf:
        return get_jaeger_exporter_protobuf(agent_host, agent_port, collector_endpoint)
    elif exporter == TracingExporterType.Otlp:
        return get_otlp_exporter(collector_endpoint)
    elif exporter == TracingExporterType.Console:
        return get_console_exporter()
    else:
        return get_console_exporter()

def get_zipkin_exporter_protobuf(collector_endpoint: str):
    from opentelemetry.exporter.zipkin.proto.http import ZipkinExporter
    zipkin_exporter = ZipkinExporter(endpoint=collector_endpoint)
    return zipkin_exporter

def get_zipkin_exporter_json(collector_endpoint: str):
    from opentelemetry.exporter.zipkin.json import ZipkinExporter
    zipkin_exporter = ZipkinExporter(endpoint=collector_endpoint)
    return zipkin_exporter

def get_jaeger_exporter_thrift(agent_host: str, agent_port: int, collector_endpoint: str = None):
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    jaeger_exporter = JaegerExporter(
        agent_host_name=agent_host,
        agent_port=agent_port,
        collector_endpoint=collector_endpoint,
        # username=xxxx, # optional
        # password=xxxx, # optional
        # max_tag_value_length=None # optional
        )
    return jaeger_exporter

def get_jaeger_exporter_protobuf(collector_endpoint: str = None):
    from opentelemetry.exporter.jaeger.proto.grpc import JaegerExporter
    jaeger_exporter = JaegerExporter(
        collector_endpoint=collector_endpoint,
        insecure=True, # optional
        # credentials=xxx # optional channel creds
        # max_tag_value_length=None # optional
        )
    return jaeger_exporter

def get_otlp_exporter(collector_endpoint: str):
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    otlp_exporter = OTLPSpanExporter(endpoint=collector_endpoint, insecure=True)
    return otlp_exporter

def get_console_exporter():
    from opentelemetry.sdk.trace.export import ConsoleSpanExporter
    console_exporter = ConsoleSpanExporter()
    return console_exporter
