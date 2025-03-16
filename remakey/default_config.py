from remakey.enums import EventsEnum, KeyNames, ModifierFlagsEnum
from remakey.remap_layer import ActionsEnum, Config, LayerMapping, Layer, MappingType

global_mapping: MappingType = {
    KeyNames.RIGHT_SHIFT: {
        "action": {
            "type": ActionsEnum.INVOKE_COMMAND,
            "value": "~/Desktop/remakey/remakey/templates/start_electron.sh",
            "event": EventsEnum.KEY_DOWN,
        }
    },
    KeyNames.END: {
        "action": {
            "type": ActionsEnum.INVOKE_COMMAND,
            "value": "~/Desktop/remakey/remakey/templates/start_electron.sh",
            "event": EventsEnum.KEY_DOWN,
        }
    },
    KeyNames.PAGE_DOWN: {
        "action": {
            "type": ActionsEnum.LAYER_DOWN,
            "value": 1,
            "event": EventsEnum.KEY_DOWN,
        },
    },
    KeyNames.PAGE_UP: {
        "action": {
            "type": ActionsEnum.LAYER_UP,
            "value": 1,
            "event": EventsEnum.KEY_DOWN,
        },
    },
    KeyNames.HOME: {
        "action": {
            "type": ActionsEnum.SET_LAYER,
            "value": 0,
            "event": EventsEnum.KEY_DOWN,
        },
    },
}


LAYER_0 = Layer(
    LayerMapping(mapping={**global_mapping}),
    name="Base layer",
    id="5a62a6a4-06d6-4f4d-99b3-afa91d311c9e",
)
LAYER_1 = Layer(
    LayerMapping(
        mapping={
            **global_mapping,
            KeyNames.X: KeyNames.ONE,
            KeyNames.C: KeyNames.TWO,
            KeyNames.V: KeyNames.THREE,
            KeyNames.S: KeyNames.FOUR,
            KeyNames.D: KeyNames.FIVE,
            KeyNames.F: KeyNames.SIX,
            KeyNames.W: KeyNames.SEVEN,
            KeyNames.E: KeyNames.EIGHT,
            KeyNames.R: KeyNames.NINE,
            KeyNames.B: KeyNames.BACKSLASH,
            KeyNames.G: KeyNames.EQUAL,
            KeyNames.T: KeyNames.RIGHT_BRACKET,
            KeyNames.Q: KeyNames.LEFT_BRACKET,
        }
    ),
    name="Numbers",
    id="5a62a6a4-06d6-4f4d-99b3-afa91d311111",
)
LAYER_2 = Layer(
    LayerMapping(
        mapping={
            **global_mapping,
            KeyNames.J: {
                "action": {
                    "type": ActionsEnum.REMAP,
                    "value": KeyNames.NINE,
                    "event": EventsEnum.KEY_DOWN,
                    "modifiers": {ModifierFlagsEnum.SHIFT},
                }
            },
        }
    ),
    name="Symbols",
    id="5a62a6a4-06d6-4f4d-99b3-afa91d3111114",
)

custom_config = Config(
    [LAYER_0, LAYER_1, LAYER_2],
    KeyNames.RIGHT_SHIFT,
    is_silent=False,
)
