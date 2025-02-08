from enum import Enum


def serialize_layer_mapping(mapping):
    """Convert LayerMapping dictionary to a string with enum names instead of values."""

    def convert_value(value):
        if isinstance(value, dict):  # Recursive conversion for nested dictionaries
            return {k: convert_value(v) for k, v in value.items()}
        elif isinstance(value, list):  # Convert lists
            return [convert_value(v) for v in value]
        elif isinstance(value, Enum):  # Replace Enums with their names
            return value.name
        return value  # Keep other values unchanged

    serialized_mapping = {
        key.name: convert_value(value) for key, value in mapping.items()
    }

    return serialized_mapping
