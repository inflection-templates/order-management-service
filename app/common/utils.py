import json
import uuid
from pygments import highlight, lexers, formatters

from app.domain_types.miscellaneous.exceptions import UUIDValidationError

def print_colorized_json(obj):
    jsonStr = json.dumps(obj.__dict__, default=str, indent=2)
    colored = highlight(jsonStr, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colored)

def validate_uuid4(uuid_str):
    try:
        val = uuid.UUID(uuid_str, version=4)
    except ValueError:
        raise UUIDValidationError("{uuid_str} is not valid UUID.")
    return uuid_str

def generate_uuid4():
    return str(uuid.uuid4())

