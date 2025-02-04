from enum import Enum
from typing import TypedDict
from enums import KEY_NAMES, KeyNames


class ActionsEnum(str, Enum):
    SET_LAYER = 1
    CHORD = 2


class KeyActionConfiguration(TypedDict):
    type: ActionsEnum | None
    value: int | KeyNames | list[KeyNames] | None


class KeyConfiguration(TypedDict):
    remap: KeyNames | list[KeyNames] | None
    action: KeyActionConfiguration | None


class LayerMapping(TypedDict):
    mapping: dict[KeyNames, KeyConfiguration, int | KeyNames | list[KeyNames] | None]


class Layer:
    def __init__(self, mapping: LayerMapping | None):
        self.mapping = LayerMapping(mapping={})

        if mapping != None:
            self.mapping = mapping


class Config:
    def __init__(
        self,
        layers: list[Layer],
        change_layer_key: KeyNames,
        suppress_original=False,
        is_silent=True,
    ):
        self.is_silent = is_silent
        self.current_layer = 0
        self.suppress_original = suppress_original
        self.layers = [Layer(None)]
        self.change_layer_key = KeyNames.BACKSLASH

        if change_layer_key is not None:
            self.change_layer_key = change_layer_key

        for layer in layers:
            self.add_layer(layer)

    def add_layer(self, layer: Layer):
        self.layers.append(layer)

    def set_current_layer(self, layer: int):
        self.current_layer = layer

    def rotate_current_layers(self):
        self.current_layer = (self.current_layer + 1) % len(self.layers)

    def check_key_in_mapping(self, keycode: KeyNames):
        return keycode in self.layers[self.current_layer].mapping.get("mapping")

    def get_remapped_value(self, keycode: KeyNames):
        return (
            self.layers[self.current_layer].mapping.get("mapping")[keycode].remap.value
        )

    def get_key_action(self, keycode: KeyNames):
        return (
            self.layers[self.current_layer].mapping.get("mapping")[keycode].remap.action
        )

    def get_key_name(self, keycode: int):
        """Get the readable key name from its keycode."""
        return KEY_NAMES.get(keycode, f"Unknown ({keycode})")
