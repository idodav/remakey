from enums import KeyNames
from remap_layer import LayerMapping, Layer, Config


LAYER_1 = Layer(
    LayerMapping(
        mapping={
            KeyNames.LEFT_ARROW: {
                "action": {
                    "type": "SET_LAYER",
                    "value": 0,
                },
            },
            KeyNames.DOWN_ARROW: {
                "action": {
                    "type": "SET_LAYER",
                    "value": 1,
                },
            },
            KeyNames.RIGHT_ARROW: {
                "action": {
                    "type": "SET_LAYER",
                    "value": 2,
                },
            },
            KeyNames.W: KeyNames.UP_ARROW,
            KeyNames.A: KeyNames.LEFT_ARROW,
            KeyNames.S: KeyNames.DOWN_ARROW,
            KeyNames.D: KeyNames.LEFT_ARROW,
            KeyNames.J: KeyNames.LEFT_ARROW,
            KeyNames.K: KeyNames.DOWN_ARROW,
            KeyNames.L: KeyNames.RIGHT_ARROW,
            KeyNames.I: KeyNames.UP_ARROW,
        }
    )
)
LAYER_2 = Layer(
    LayerMapping(
        mapping={
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
    [LAYER_1, LAYER_2], KeyNames.BACKSLASH, is_silent=False, suppress_original=False
)
