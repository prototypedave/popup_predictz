# Data util function
from dataclasses import is_dataclass, fields

def has_none_values(instance) -> bool:
    if not is_dataclass(instance):
        raise TypeError("Provided instance is not a dataclass.")

    return any(getattr(instance, field.name) is None for field in fields(instance))