from enum import Enum
from typing import TypedDict
from enums import KEY_NAMES, KeyNames


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
        suppress_original=False,
        is_silent=True,
    ):
        self.is_silent = is_silent
        self.current_layer = None
        self.suppress_original = suppress_original
        self.layers = []
        self.change_layer_key = KeyNames.BACKSLASH

        if change_layer_key is not None:
            self.change_layer_key = change_layer_key

        for layer in layers:
            self.add_layer(layer)

        if len(self.layers) > 0:
            self.current_layer = 0

    def add_layer(self, layer: Layer):
        self.layers.append(layer)

    def set_current_layer(self, layer: int):
        if self.current_layer is not None:
            self.current_layer = layer

    def rotate_current_layers(self):
        if self.current_layer is not None:
            self.current_layer = (self.current_layer + 1) % len(self.layers)

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

    def get_key_action(self, keycode: KeyNames):
        try:
            dict_item = self.layers[self.current_layer].mapping.get("mapping")[keycode]
            dict_item: KeyConfiguration = KeyConfiguration(**dict_item)
            return dict_item.get("action")
        except Exception as e:
            return {}

    def get_key_name(self, keycode: int):
        """Get the readable key name from its keycode."""
        return KEY_NAMES.get(keycode, f"Unknown ({keycode})")
