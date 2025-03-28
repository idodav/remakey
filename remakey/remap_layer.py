from enum import Enum
import json
from typing import Optional, TypedDict
from uuid import uuid4

from remakey.enums import KEY_NAMES, EventsEnum, KeyNames, ModifierFlagsEnum


class ActionsEnum(str, Enum):
    REMAP = 0
    SET_LAYER = 1
    CHORD = 2
    SET_MOUSE_POSITION = 3
    SET_MOUSE_POSITION_X = 4
    SET_MOUSE_POSITION_Y = 5
    SET_MOUSE_POSITION_XY = 6
    INC_MOUSE_POSITION_X = 7
    INC_MOUSE_POSITION_Y = 8
    INVOKE_COMMAND = 9
    SET_MODIFIER = 10
    LAYER_UP = 11
    LAYER_DOWN = 12


class KeyActionConfiguration(TypedDict):
    type: ActionsEnum | None
    value: str | int | KeyNames | list[KeyNames] | None
    event: EventsEnum | None
    modifiers: Optional[list[str | ModifierFlagsEnum]]


class KeyConfiguration(TypedDict):
    action: KeyActionConfiguration | None


MappingType = dict[
    KeyNames,
    KeyConfiguration
    | int
    | KeyNames
    | list[KeyNames]
    | list[KeyConfiguration]
    | dict
    | None,
]


class LayerMapping(TypedDict):
    mapping: MappingType


class LayerMappingSerializer:
    @classmethod
    def to_json(cls, mapping):
        def serialize(obj):
            if isinstance(obj, Enum):
                return obj.name
            if isinstance(obj, KeyConfiguration):
                return {"action": serialize(obj.action)}
            if isinstance(obj, KeyActionConfiguration):
                return {
                    "type": obj.type.name,
                    "value": obj.value,
                    "event": obj.event.name,
                    "modifiers": (
                        [mod.name for mod in obj.modifiers] if obj.modifiers else None
                    ),
                }
            return obj

        return json.dumps(mapping, default=serialize, indent=4)

    @classmethod
    def from_json(cls, json_str: str) -> LayerMapping:
        def deserialize(obj):
            if isinstance(obj, str):
                try:
                    return KeyNames(obj)
                except KeyError:
                    try:
                        return ActionsEnum(obj)
                    except KeyError:
                        try:
                            return EventsEnum(obj)
                        except KeyError:
                            try:
                                return ModifierFlagsEnum(obj)
                            except KeyError:
                                return obj
            if isinstance(obj, dict):
                if "action" in obj:
                    return KeyConfiguration(
                        action=KeyActionConfiguration(
                            type=ActionsEnum(obj["action"]["type"]),
                            value=obj["action"]["value"],
                            event=EventsEnum(obj["action"]["event"]),
                            modifiers=(
                                [
                                    ModifierFlagsEnum(mod)
                                    for mod in obj["action"]["modifiers"]
                                ]
                                if obj["action"]["modifiers"]
                                else None
                            ),
                        )
                    )
            return obj

        return json.loads(json_str, object_hook=deserialize)


class Layer:
    def __init__(
        self,
        mapping: LayerMapping | None,
        name: str | None = None,
        id: str | None = None,
        suppress_unmapped=False,
    ):
        self.id = id if id is not None else uuid4()
        self.mapping = LayerMapping(mapping={})
        self.suppress_unmapped = suppress_unmapped

        if name != None:
            self.name = name
        else:
            self.name = self.id

        if mapping != None:
            self.check_loops(mapping)
            self.mapping = mapping

    def check_loops(self, mapping: LayerMapping):
        """Detect loops in key mappings by checking if a key is remapped back to itself or another mapped key."""
        keys = set(mapping.get("mapping").keys())  # Extract all mapped keys
        values = set()  # Extract all mapped values

        for key, value in mapping.get("mapping").items():
            if isinstance(value, dict) and "action" in value:
                action_type = value["action"].get("type")
                action_value = value["action"].get("value")

                if action_type == ActionsEnum.CHORD:
                    # If any key in the chord is also a mapped key, it's a loop
                    for k in action_value:
                        values.add(k)
            elif isinstance(value, list):
                for item in value:
                    action_type = item["action"].get("type")
                    action_value = item["action"].get("value")

                    if action_type == ActionsEnum.CHORD:
                        # If any key in the chord is also a mapped key, it's a loop
                        for k in action_value:
                            if isinstance(k, dict):
                                values.add(k.get("keycode"))
                            elif isinstance(k, KeyNames):
                                values.add(k)
            else:
                # If the value is a direct key mapping, store it for loop detection
                values.add(value)

        # Check if any mapped key appears in the values, indicating a remap loop
        if keys & values:
            raise ValueError(
                f"❌ Loop detected! Some keys map to other mapped keys: {keys & values}"
            )

        print("✅ No loops detected in the key mapping.")


class Config:
    def __init__(
        self,
        layers: list[Layer],
        change_layer_key: KeyNames,
        is_silent=True,
    ):
        self.is_silent: bool = is_silent
        self.current_layer: int | None = None
        self.layers: list[Layer] = []
        self.change_layer_key = KeyNames.BACKSLASH

        if change_layer_key is not None:
            self.change_layer_key = change_layer_key

        for layer in layers:
            self.add_layer(layer)

        if len(self.layers) > 0:
            self.current_layer = 0

    def add_layer(self, layer: Layer):
        self.layers.append(layer)

    def get_current_layer(self) -> Layer:
        return self.layers[self.current_layer]

    def set_current_layer(self, layer: int):
        if self.current_layer is not None:
            self.current_layer = layer

    def set_current_layer_by_id(self, layer_id: str):
        for i, layer in enumerate(self.layers):
            if layer.id == layer_id:
                self.set_current_layer(i)

    def rotate_current_layers(self, direction=1):
        if self.current_layer is not None:
            self.current_layer = (self.current_layer + (1 * direction)) % len(
                self.layers
            )

    def check_key_in_mapping(self, keycode: KeyNames):
        if self.current_layer is not None:
            return keycode in self.layers[self.current_layer].mapping.get("mapping")

    def get_remapped_value(self, keycode: KeyNames):
        dict_item = self.layers[self.current_layer].mapping.get("mapping")[keycode]
        if type(dict_item) == KeyConfiguration:
            dict_item: KeyConfiguration = dict_item
            if dict_item.action is not None:
                if dict_item.action.type == ActionsEnum.REMAP:
                    return dict_item.action.value
        elif type(dict_item) == KeyNames:
            return dict_item
        elif type(dict_item) == list:
            return None
        return None

    def get_key_action(self, keycode: KeyNames, event_type: EventsEnum):
        try:
            dict_item = self.layers[self.current_layer].mapping.get("mapping")[keycode]

            if isinstance(dict_item, dict):
                return dict_item.get("action")
            if isinstance(dict_item, list):
                action_by_event = [
                    action
                    for action in dict_item
                    if action.get("action").get("event") == event_type
                ]
                return action_by_event[0].get("action") if action_by_event else None
            return dict_item.get("action")
        except Exception as e:
            return None

    def get_key_events(self, keycode: KeyNames):
        try:
            dict_item = self.layers[self.current_layer].mapping.get("mapping")[keycode]

            if isinstance(dict_item, dict):
                return [dict_item.get("action").get("event")]
            if isinstance(dict_item, list):
                result = []
                for item in dict_item:
                    result.append(item.get("action").get("event"))
                return result
            return []
        except Exception as e:
            return {}

    def get_key_name(self, keycode: int):
        """Get the readable key name from its keycode."""
        return KEY_NAMES.get(keycode, f"Unknown ({keycode})")

    def get_layer_names(self):
        return [layer.name for layer in self.layers]

    def get_layer_ids(self):
        return [layer.id for layer in self.layers]

    def get_layer(self, layer_id):
        for layer in self.layers:
            if layer.id == layer_id:
                return layer
        return None

    def add_remap_to_layer(self, layer_id, key, value):
        layer = self.get_layer(layer_id)
        if layer is not None:
            layer.mapping["mapping"][key] = value
