from pydantic import BaseModel, root_validator
from typing import Dict, Any


class StrictBaseModel(BaseModel):
    "Base model with strict validation applied"
    
    class Config:
        validate_assignment = True
        arbitrary_types_allowed = False
        validate_all = True

    @root_validator(pre=True)
    def validate_types(cls, values):
        "Validate types before any conversion happens"
        errors = []
        
        # Define field type mappings for common fields
        string_fields = []
        boolean_fields = []
        integer_fields = []
        float_fields = []
        
        # Get field types from the model
        field_types = cls.__annotations__
        
        for field_name, field_type in field_types.items():
            # Handle Optional types
            if hasattr(field_type, '__origin__') and field_type.__origin__ is type(None).__class__:
                # Get the actual type from Optional[Type]
                actual_type = field_type.__args__[0]
                if actual_type == str:
                    string_fields.append(field_name)
                elif actual_type == bool:
                    boolean_fields.append(field_name)
                elif actual_type == int:
                    integer_fields.append(field_name)
                elif actual_type == float:
                    float_fields.append(field_name)
            else:
                # Direct types
                if field_type == str:
                    string_fields.append(field_name)
                elif field_type == bool:
                    boolean_fields.append(field_name)
                elif field_type == int:
                    integer_fields.append(field_name)
                elif field_type == float:
                    float_fields.append(field_name)
        
        # Validate each field
        for field_name, field_value in values.items():
            if field_value is None:
                continue
                
            if field_name in string_fields and not isinstance(field_value, str):
                errors.append(f"Field '{field_name}' must be a string, got {type(field_value).__name__}")
            elif field_name in boolean_fields and not isinstance(field_value, bool):
                errors.append(f"Field '{field_name}' must be a boolean, got {type(field_value).__name__}")
            elif field_name in integer_fields and not isinstance(field_value, int):
                errors.append(f"Field '{field_name}' must be an integer, got {type(field_value).__name__}")
            elif field_name in float_fields and not isinstance(field_value, float):
                errors.append(f"Field '{field_name}' must be a float, got {type(field_value).__name__}")
        
        if errors:
            raise ValueError("; ".join(errors))
        
        return values
        