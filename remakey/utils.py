from enum import Enum


def serialize_layer_mapping(mapping):
    """Convert LayerMapping dictionary to a string with enum names instead of values."""

    def convert_value(value):
        if isinstance(value, dict):  # Recursive conversion for nested dictionaries
            translated_action = value["action"]["type"].name
            parsed_value = value["action"]["value"]
            res = {"action": {"type": translated_action, "value": parsed_value}}

            return res
        elif isinstance(value, list):  # Convert lists
            return convert_value(value[0])
        return value  # Keep other values unchanged

    serialized_mapping = {key: convert_value(value) for key, value in mapping.items()}

    return serialized_mapping
