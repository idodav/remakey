from remakey.enums import EventsEnum, KeyNames
from remakey.remap_layer import ActionsEnum, Config, LayerMapping, Layer

global_mapping = {
    KeyNames.KEYPAD_0: {
        "action": {
            "type": ActionsEnum.INVOKE_COMMAND,
            "value": "~/Desktop/remakey/remakey/templates/start_electron.sh",
            "event": EventsEnum.KEY_DOWN,
        }
    },
    KeyNames.RIGHT_COMMAND: {
        "action": {
            "type": ActionsEnum.SET_LAYER,
            "value": 0,
            "event": EventsEnum.KEY_DOWN,
        },
    },
    KeyNames.RIGHT_OPTION: {
        "action": {
            "type": ActionsEnum.SET_LAYER,
            "value": 1,
            "event": EventsEnum.KEY_DOWN,
        },
    },
    KeyNames.RIGHT_CONTROL: {
        "action": {
            "type": ActionsEnum.SET_LAYER,
            "value": 2,
            "event": EventsEnum.KEY_DOWN,
        },
    },
    KeyNames.S: {
        "action": {
            "type": ActionsEnum.REMAP,
            "value": KeyNames.A,
            "modifiers": ["command"],
            "event": EventsEnum.KEY_HOLD,
        }
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
            KeyNames.J: KeyNames.DOWN_ARROW,
            KeyNames.K: KeyNames.UP_ARROW,
            KeyNames.L: KeyNames.RIGHT_ARROW,
            KeyNames.H: KeyNames.LEFT_ARROW,
        }
    ),
    name="Navigation layer",
    id="5a62a6a4-06d6-4f4d-99b3-afa91d311123",
)
LAYER_2 = Layer(
    LayerMapping(
        mapping={
            **global_mapping,
            KeyNames.A: KeyNames.ONE,
            KeyNames.S: KeyNames.TWO,
            KeyNames.D: KeyNames.THREE,
            KeyNames.F: KeyNames.FOUR,
            KeyNames.G: KeyNames.FIVE,
            KeyNames.H: KeyNames.SIX,
            KeyNames.J: KeyNames.SEVEN,
            KeyNames.K: KeyNames.EIGHT,
            KeyNames.L: KeyNames.NINE,
            KeyNames.SEMICOLON: KeyNames.ZERO,
            KeyNames.Q: KeyNames.F1,
            KeyNames.W: KeyNames.F2,
            KeyNames.E: KeyNames.F3,
            KeyNames.R: KeyNames.F4,
            KeyNames.T: KeyNames.F5,
            KeyNames.Y: KeyNames.F6,
            KeyNames.U: KeyNames.F7,
            KeyNames.I: KeyNames.F8,
            KeyNames.O: KeyNames.F9,
            KeyNames.P: KeyNames.F10,
            KeyNames.LEFT_BRACKET: KeyNames.F11,
            KeyNames.RIGHT_BRACKET: KeyNames.F12,
        }
    ),
    name="Number layer",
    id="5a62a6a4-06d6-4f4d-99b3-afa91d311111",
)

custom_config = Config(
    [LAYER_0, LAYER_1, LAYER_2],
    KeyNames.RIGHT_SHIFT,
    is_silent=False,
)
