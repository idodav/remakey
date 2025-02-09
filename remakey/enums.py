from enum import Enum, IntEnum
import Quartz


class FunctionKeys(IntEnum):
    F1 = 122
    F2 = 120
    F3 = 99
    F4 = 118
    F5 = 96
    F6 = 97
    F7 = 98
    F8 = 100
    F9 = 101
    F10 = 109
    F11 = 103
    F12 = 111


class KeyNames(IntEnum):
    A = 0
    S = 1
    D = 2
    F = 3
    H = 4
    G = 5
    Z = 6
    X = 7
    C = 8
    V = 9
    SECTION = 10
    B = 11
    Q = 12
    W = 13
    E = 14
    R = 15
    Y = 16
    T = 17
    ONE = 18
    TWO = 19
    THREE = 20
    FOUR = 21
    SIX = 22
    FIVE = 23
    EQUAL = 24
    NINE = 25
    SEVEN = 26
    MINUS = 27
    EIGHT = 28
    ZERO = 29
    RIGHT_BRACKET = 30
    O = 31
    U = 32
    LEFT_BRACKET = 33
    I = 34
    P = 35
    RETURN = 36
    L = 37
    J = 38
    APOSTROPHE = 39
    K = 40
    SEMICOLON = 41
    BACKSLASH = 42
    COMMA = 43
    SLASH = 44
    N = 45
    M = 46
    PERIOD = 47
    TAB = 48
    SPACE = 49
    BACKSPACE = 51
    ESCAPE = 53
    LEFT_SHIFT = 56
    RIGHT_COMMAND = 54
    LEFT_COMMAND = 55
    CAPS_LOCK = 57
    LEFT_OPTION = 58
    LEFT_CONTROL = 59
    RIGHT_SHIFT = 60
    RIGHT_OPTION = 61
    RIGHT_CONTROL = 62
    FUNCTION = 63
    F17 = 64
    KEYPAD_DOT = 65
    KEYPAD_ASTERISK = 67
    KEYPAD_PLUS = 69
    KEYPAD_CLEAR = 71
    KEYPAD_SLASH = 75
    KEYPAD_ENTER = 76
    KEYPAD_MINUS = 78
    F18 = 79
    F19 = 80
    KEYPAD_EQUAL = 81
    KEYPAD_0 = 82
    KEYPAD_1 = 83
    KEYPAD_2 = 84
    KEYPAD_3 = 85
    KEYPAD_4 = 86
    KEYPAD_5 = 87
    KEYPAD_6 = 88
    KEYPAD_7 = 89
    KEYPAD_8 = 91
    KEYPAD_9 = 92
    F3 = 99
    F5 = 96
    F6 = 97
    F7 = 98
    F8 = 100
    F9 = 101
    F13 = 105
    F16 = 106
    F14 = 107
    F10 = 109
    F11 = 103
    F12 = 111
    F15 = 113
    HOME = 115
    PAGE_UP = 116
    FORWARD_DELETE = 117
    F4 = 118
    END = 119
    F2 = 120
    PAGE_DOWN = 121
    F1 = 122
    LEFT_ARROW = 123
    RIGHT_ARROW = 124
    DOWN_ARROW = 125
    UP_ARROW = 126
    BRIGHTNESS_DOWN = 145
    BRIGHTNESS_UP = 144
    UNKNOWN = 160
    FN = 179


KEY_NAMES = {
    0: "A",
    1: "S",
    2: "D",
    3: "F",
    4: "H",
    5: "G",
    6: "Z",
    7: "X",
    8: "C",
    9: "V",
    10: "§",
    11: "B",
    12: "Q",
    13: "W",
    14: "E",
    15: "R",
    16: "Y",
    17: "T",
    18: "1",
    19: "2",
    20: "3",
    21: "4",
    22: "6",
    23: "5",
    24: "=",
    25: "9",
    26: "7",
    27: "-",
    28: "8",
    29: "0",
    30: "]",
    31: "O",
    32: "U",
    33: "[",
    34: "I",
    35: "P",
    36: "Return",
    37: "L",
    38: "J",
    39: "'",
    40: "K",
    41: ";",
    42: "\\",
    43: ",",
    44: "/",
    45: "N",
    46: "M",
    47: ".",
    48: "Tab",
    49: "Space",
    50: "`",
    51: "Backspace",
    53: "Escape",
    54: "Right Command",
    55: "Left Command",
    56: "Left Shift",
    57: "Caps Lock",
    58: "Left Option",
    59: "Left Control",
    60: "Right Shift",
    61: "Right Option",
    62: "Right Control",
    63: "Function",
    64: "Keypad F17",
    65: "Keypad .",
    67: "Keypad *",
    69: "Keypad +",
    71: "Keypad Clear",
    75: "Keypad /",
    76: "Keypad Enter",
    78: "Keypad -",
    79: "F18",
    80: "F19",
    81: "Keypad =",
    82: "Keypad 0",
    83: "Keypad 1",
    84: "Keypad 2",
    85: "Keypad 3",
    86: "Keypad 4",
    87: "Keypad 5",
    88: "Keypad 6",
    89: "Keypad 7",
    91: "Keypad 8",
    92: "Keypad 9",
    99: "F3",
    96: "F5",
    97: "F6",
    98: "F7",
    100: "F8",
    101: "F9",
    105: "F13",
    106: "F16",
    107: "F14",
    109: "F10",
    103: "F11",
    111: "F12",
    113: "F15",
    115: "Home",
    116: "Page Up",
    117: "Forward Delete",
    118: "F4",
    119: "End",
    120: "F2",
    121: "Page Down",
    122: "F1",
    123: "Left Arrow",
    124: "Right Arrow",
    125: "Down Arrow",
    126: "Up Arrow",
    145: "Brightness Down",
    144: "Brightness Up",
    160: "UNKNOWN",
    179: "fn",
}

# Modifier Key Mapping
MODIFIERS = {
    Quartz.kCGEventFlagMaskShift: "Shift",
    Quartz.kCGEventFlagMaskControl: "Ctrl",
    Quartz.kCGEventFlagMaskCommand: "Cmd",
    Quartz.kCGEventFlagMaskAlternate: "Option",
}

MODIFIER_FLAGS = {
    "shift": Quartz.kCGEventFlagMaskShift,
    "control": Quartz.kCGEventFlagMaskControl,
    "alt": Quartz.kCGEventFlagMaskAlternate,
    "command": Quartz.kCGEventFlagMaskCommand,
}


class ModifierFlagsEnum(str, Enum):
    SHIFT = "shift"
    CONTROL = "control"
    ALT = "alt"
    COMMAND = "command"


MODIFIER_KEY_TO_BITMASK = {
    KeyNames.LEFT_SHIFT: Quartz.kCGEventFlagMaskShift,
    KeyNames.RIGHT_SHIFT: Quartz.kCGEventFlagMaskShift,
    KeyNames.LEFT_CONTROL: Quartz.kCGEventFlagMaskControl,
    KeyNames.RIGHT_CONTROL: Quartz.kCGEventFlagMaskControl,
    KeyNames.LEFT_COMMAND: Quartz.kCGEventFlagMaskCommand,
    KeyNames.RIGHT_COMMAND: Quartz.kCGEventFlagMaskCommand,
    KeyNames.LEFT_OPTION: Quartz.kCGEventFlagMaskAlternate,
    KeyNames.RIGHT_OPTION: Quartz.kCGEventFlagMaskAlternate,
    KeyNames.FUNCTION: 0x00800000,
    KeyNames.CAPS_LOCK: 0x00010000,
}

# Function Key Mapping (F1 - F12)
FUNCTION_KEYS = {
    56: "Left Shift",
    57: "Caps Lock",
    60: "Right Shift",
    61: "Option",
    122: "F1",
    120: "F2",
    99: "F3",
    118: "F4",
    96: "F5",
    97: "F6",
    98: "F7",
    100: "F8",
    101: "F9",
    109: "F10",
    103: "F11",
    111: "F12",
}


class EventsEnum(str, Enum):
    KEY_DOWN = Quartz.kCGEventKeyDown
    KEY_UP = Quartz.kCGEventKeyUp
    KEY_HOLD = "KEY_HOLD"
    DOUBLE_CLICK = "DOUBLE_CLICK"
    TRIPLE_CLICK = "TRIPLE_CLICK"
