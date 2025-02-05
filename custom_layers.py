from enums import KeyNames, EventsEnum
from remap_layer import ActionsEnum, Config, LayerMapping, Layer

LAYER_0 = Layer(
    LayerMapping(
        mapping={
            KeyNames.RIGHT_COMMAND: {
                "action": {
                    "type": ActionsEnum.SET_LAYER,
                    "value": 0,
                },
            },
            KeyNames.RIGHT_OPTION: {
                "action": {
                    "type": ActionsEnum.SET_LAYER,
                    "value": 1,
                },
            },
            KeyNames.RIGHT_CONTROL: {
                "action": {
                    "type": ActionsEnum.SET_LAYER,
                    "value": 2,
                }
            },
        }
    )
)
LAYER_1 = Layer(
    LayerMapping(
        mapping={
            KeyNames.RIGHT_COMMAND: {
                "action": {
                    "type": ActionsEnum.SET_LAYER,
                    "value": 0,
                },
            },
            KeyNames.RIGHT_OPTION: {
                "action": {
                    "type": ActionsEnum.SET_LAYER,
                    "value": 1,
                },
            },
            KeyNames.RIGHT_CONTROL: {
                "action": {
                    "type": ActionsEnum.SET_LAYER,
                    "value": 2,
                },
            },
            KeyNames.W: KeyNames.UP_ARROW,
            KeyNames.A: KeyNames.LEFT_ARROW,
            KeyNames.S: KeyNames.DOWN_ARROW,
            KeyNames.D: KeyNames.RIGHT_ARROW,
            KeyNames.J: KeyNames.LEFT_ARROW,
            KeyNames.K: KeyNames.DOWN_ARROW,
            KeyNames.L: KeyNames.RIGHT_ARROW,
            KeyNames.I: KeyNames.UP_ARROW,
            KeyNames.KEYPAD_4: {
                "action": {
                    "type": ActionsEnum.SET_MOUSE_POSITION_XY,
                    "value": (100, 500),
                }
            },
            KeyNames.KEYPAD_5: {
                "action": {
                    "type": ActionsEnum.SET_MOUSE_POSITION_XY,
                    "value": (950, 500),
                }
            },
            KeyNames.KEYPAD_6: {
                "action": {
                    "type": ActionsEnum.SET_MOUSE_POSITION_XY,
                    "value": (1900, 500),
                }
            },
            KeyNames.KEYPAD_7: {
                "action": {
                    "type": ActionsEnum.SET_MOUSE_POSITION_XY,
                    "value": (100, 100),
                }
            },
            KeyNames.KEYPAD_8: {
                "action": {
                    "type": ActionsEnum.SET_MOUSE_POSITION_XY,
                    "value": (950, 100),
                }
            },
            KeyNames.KEYPAD_9: {
                "action": {
                    "type": ActionsEnum.SET_MOUSE_POSITION_XY,
                    "value": (1900, 100),
                }
            },
            KeyNames.KEYPAD_1: {
                "action": {
                    "type": ActionsEnum.SET_MOUSE_POSITION_XY,
                    "value": (100, 950),
                }
            },
            KeyNames.KEYPAD_2: {
                "action": {
                    "type": ActionsEnum.SET_MOUSE_POSITION_XY,
                    "value": (950, 950),
                }
            },
            KeyNames.KEYPAD_3: {
                "action": {
                    "type": ActionsEnum.SET_MOUSE_POSITION_XY,
                    "value": (1900, 950),
                }
            },
            KeyNames.UP_ARROW: {
                "action": {
                    "type": ActionsEnum.INC_MOUSE_POSITION_Y,
                    "value": -10,
                }
            },
            KeyNames.DOWN_ARROW: {
                "action": {
                    "type": ActionsEnum.INC_MOUSE_POSITION_Y,
                    "value": 10,
                }
            },
            KeyNames.LEFT_ARROW: {
                "action": {
                    "type": ActionsEnum.INC_MOUSE_POSITION_X,
                    "value": -10,
                }
            },
            KeyNames.RIGHT_ARROW: {
                "action": {
                    "type": ActionsEnum.INC_MOUSE_POSITION_X,
                    "value": 10,
                }
            },
        }
    )
)
LAYER_2 = Layer(
    LayerMapping(
        mapping={
            KeyNames.RIGHT_COMMAND: {
                "action": {
                    "type": ActionsEnum.SET_LAYER,
                    "value": 0,
                },
            },
            KeyNames.RIGHT_OPTION: {
                "action": {
                    "type": ActionsEnum.SET_LAYER,
                    "value": 1,
                },
            },
            KeyNames.RIGHT_CONTROL: {
                "action": {
                    "type": ActionsEnum.SET_LAYER,
                    "value": 2,
                },
            },
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
    )
)

custom_config = Config(
    [LAYER_0, LAYER_1, LAYER_2],
    KeyNames.BACKSLASH,
    is_silent=False,
    suppress_original=False,
)
