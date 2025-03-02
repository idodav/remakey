import time
import subprocess
import Quartz
import threading
import queue

from remakey.default_config import custom_config
from remakey.enums import (
    MODIFIER_FLAGS,
    MODIFIER_KEY_TO_BITMASK,
    MODIFIERS,
    EventsEnum,
    KeyNames,
)
from remakey.remap_layer import ActionsEnum, Config, KeyActionConfiguration


class KeyLogger:
    def __init__(self, config: Config):
        self.start_event = threading.Event()
        self.stop_event = threading.Event()
        self.data_queue = queue.Queue()
        self.change_layer_queue = queue.Queue()
        self.config: Config = config
        self.is_silent = self.config.is_silent
        self.counters = {}
        self.key_press_times = {}
        self.hold_threshold = 0.5

    def log(self, text):
        if self.is_silent:
            return
        print(text)

    def stop_keylogger(self):
        self.log("🛑 Stopping Key Logger")
        Quartz.CFRunLoopStop(Quartz.CFRunLoopGetCurrent())

        self.start_event.clear()
        self.stop_event.clear()

        while True:
            if self.start_event.is_set():
                break
            time.sleep(0.1)

        self.start_key_logger_threaded()

    def send_key_event(self, keycode, event_type, modifier_flags=None):
        """Send a new keyboard event with the specified keycode."""
        event = Quartz.CGEventCreateKeyboardEvent(
            None, keycode, event_type == Quartz.kCGEventKeyDown
        )

        if modifier_flags:
            Quartz.CGEventSetFlags(event, modifier_flags)

        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

    def get_active_modifiers(self, flags):
        """Get active modifier keys as a list."""
        return [name for bitmask, name in MODIFIERS.items() if flags & bitmask]

    def rotate_layer(self):
        self.config.rotate_current_layers()
        current_layer_id = self.config.layers[self.config.current_layer].id
        self.log(f"🔄 Switched to Layer {self.config.current_layer}")
        self.change_layer_queue.put(current_layer_id)

    def set_layer(self, layer_index):
        self.config.set_current_layer(layer_index)
        current_layer_id = self.config.layers[self.config.current_layer].id
        current_layer_name = self.config.layers[self.config.current_layer].name
        self.log(f"🔄 Switched to Layer {current_layer_name}")
        self.change_layer_queue.put(current_layer_id)

    def set_layer_by_id(self, layer_id):
        self.config.set_current_layer_by_id(layer_id)
        current_layer_id = self.config.layers[self.config.current_layer].id
        current_layer_name = self.config.layers[self.config.current_layer].name
        self.log(f"🔄 Switched to Layer {current_layer_name}")
        self.change_layer_queue.put(current_layer_id)

    def get_current_layer(self):
        return self.config.get_current_layer()

    @staticmethod
    def keyboard_callback(proxy, event_type, event, refcon):
        """Callback function to log key presses with keycodes."""
        self_instance: KeyLogger = refcon

        if self_instance.is_programmatically_triggered(event):
            self_instance.log("🔵 Programmatically generated event detected, ignoring.")

        keycode = Quartz.CGEventGetIntegerValueField(
            event, Quartz.kCGKeyboardEventKeycode
        )
        flags = Quartz.CGEventGetFlags(event)
        active_modifiers = self_instance.get_active_modifiers(flags)
        suppress_event = False

        if event_type == Quartz.kCGEventFlagsChanged:
            try:
                keycode_modifier_flag = MODIFIER_KEY_TO_BITMASK[KeyNames(keycode)]
                generated_event = (
                    Quartz.kCGEventKeyDown
                    if keycode_modifier_flag & flags
                    else Quartz.kCGEventKeyUp
                )

                self_instance.register_event(generated_event, active_modifiers, keycode)

                if generated_event == Quartz.kCGEventKeyDown:
                    suppress_event = self_instance.handle_key_down(
                        keycode, generated_event
                    )

            except KeyError:
                print(f"Key error flags change {keycode}")
        if event_type == Quartz.kCGEventKeyDown:
            self_instance.register_event(event_type, active_modifiers, keycode)
            suppress_event = self_instance.handle_key_down(keycode, event_type)
        elif event_type == Quartz.kCGEventKeyUp:
            self_instance.register_event(event_type, active_modifiers, keycode)
            self_instance.handle_key_up(keycode)

        if self_instance.config.get_current_layer().suppress_unmapped:
            return None  # Suppress original key

        return None if suppress_event else event

    @staticmethod
    def check_stop_loop(timer, info):
        self_instance: KeyLogger = info
        if self_instance.stop_event.is_set():
            self_instance.stop_keylogger()

    def handle_flags_changed(self, flags, keycode):
        active_modifiers = self.get_active_modifiers(flags)
        self.log(f"Active modifiers: {active_modifiers}")

    def handle_key_down(self, keycode, event_type):
        return self.track_special_events(keycode) or self.handle_event(
            event_type, keycode
        )

    def handle_event(self, event_type, keycode):
        self.counters[keycode] = self.counters.get(keycode, 0) + 1

        if keycode == self.config.change_layer_key.value and event_type == int(
            EventsEnum.KEY_DOWN.value
        ):
            self.rotate_layer()
            return True  # Suppress original key
        elif self.config.check_key_in_mapping(keycode):
            action: KeyActionConfiguration | None = self.config.get_key_action(
                keycode, event_type
            )

            # Default action is remapping
            if action is None:
                new_keycode = self.config.get_remapped_value(keycode)
                if new_keycode is not None:
                    self.log(
                        f"🔁 Remapping {KeyNames(keycode).name} → {KeyNames(new_keycode).name}"
                    )
                    new_event_type = (
                        Quartz.kCGEventKeyDown
                        if event_type == Quartz.kCGEventKeyDown
                        else Quartz.kCGEventKeyUp
                    )

                    self.send_key_event(new_keycode, new_event_type)
                    return True  # Suppress original key
            else:
                action_type = action.get("type")
                action_value = action.get("value")
                action_event = action.get("event")

                if action_event is not None and str(event_type) != str(
                    action_event.value
                ):
                    return False

                if action_type == ActionsEnum.CHORD:
                    for key_tuple in action_value:
                        # TODO fix this logic
                        if isinstance(key_tuple, int):
                            self.send_key_event(key_tuple, key_tuple)
                        elif isinstance(key_tuple, dict):
                            chord_keycode = key_tuple.get("key")
                            chord_event = key_tuple.get("event")
                            custom_modifiers = key_tuple.get("modifiers")

                            modifier_flags = None

                            if custom_modifiers:
                                modifier_flags = 0
                                for modifier in custom_modifiers:
                                    modifier_flags |= MODIFIER_FLAGS[modifier]
                            self.send_key_event(
                                chord_keycode, chord_event, modifier_flags
                            )
                    return True
                elif action_type == ActionsEnum.SET_MODIFIER:
                    self.active_modifiers = action_value
                elif action_type == ActionsEnum.SET_LAYER:
                    self.set_layer(action_value)
                    return True
                elif action_type == ActionsEnum.SET_MOUSE_POSITION_X:
                    self.set_mouse_x(action_value)
                    return True
                elif action_type == ActionsEnum.SET_MOUSE_POSITION_XY:
                    (x, y) = action_value
                    self.set_mouse_position(x, y)
                    return True
                elif action_type == ActionsEnum.INC_MOUSE_POSITION_X:
                    y_inc = action_value
                    self.inc_mouse_x(y_inc)
                    return True
                elif action_type == ActionsEnum.INC_MOUSE_POSITION_Y:
                    y_inc = action_value
                    self.inc_mouse_y(y_inc)
                    return True
                elif action_type == ActionsEnum.INVOKE_COMMAND:
                    subprocess.Popen(action_value, shell=True)
                elif action_type == ActionsEnum.REMAP:
                    new_keycode = action_value
                    modifiers = action.get("modifiers")
                    modifier_flags = None

                    if modifiers:
                        modifier_flags = 0
                        for modifier in modifiers:
                            modifier_flags |= MODIFIER_FLAGS[modifier]
                    self.send_key_event(
                        new_keycode, Quartz.kCGEventKeyDown, modifier_flags
                    )
                    self.send_key_event(
                        new_keycode, Quartz.kCGEventKeyUp, modifier_flags
                    )
                    return True  # Suppress original key

                return True
        return False

    def track_special_events(self, keycode):
        now = time.time()
        key_events = self.config.get_key_events(keycode)

        if (
            EventsEnum.KEY_HOLD in key_events
            or EventsEnum.KEY_HOLD_RELEASE in key_events
        ):
            # Track key press start time
            if keycode not in self.key_press_times:
                self.key_press_times[keycode] = {"timestamp": now, "triggered": False}
            elif not self.key_press_times[keycode].get("released"):
                press_duration = now - self.key_press_times[keycode].get("timestamp")
                triggered = self.key_press_times[keycode].get("triggered")

                if press_duration >= self.hold_threshold and not triggered:
                    self.key_press_times[keycode] = {
                        "timestamp": self.key_press_times[keycode].get("timestamp"),
                        "triggered": True,
                    }
                    self.register_event(EventsEnum.KEY_HOLD.value, [], keycode)
                    self.handle_event(EventsEnum.KEY_HOLD.value, keycode)
            else:
                return False

            return True
        return False

    def handle_key_up(self, keycode):
        self.active_modifiers = []
        if keycode in self.key_press_times:
            now = time.time()
            press_duration = now - self.key_press_times[keycode].get("timestamp")
            triggered = self.key_press_times[keycode].get("triggered")

            if press_duration >= self.hold_threshold and triggered:
                del self.key_press_times[keycode]  # Remove after processing

                self.register_event(EventsEnum.KEY_HOLD_RELEASE.value, [], keycode)
                return self.handle_event(EventsEnum.KEY_HOLD_RELEASE.value, keycode)
            elif self.key_press_times[keycode].get("released"):
                del self.key_press_times[keycode]  # Remove after processing
            else:
                self.key_press_times[keycode] = {
                    "released": True,
                    "timestamp": self.key_press_times[keycode].get("timestamp"),
                    "triggered": None,
                }
                self.send_key_event(keycode, Quartz.kCGEventKeyDown)
                self.send_key_event(keycode, Quartz.kCGEventKeyUp)

        return self.handle_event(EventsEnum.KEY_UP, keycode)

    def is_programmatically_triggered(self, event):
        """Returns True if the event was generated by software."""
        source_state_id = Quartz.CGEventGetIntegerValueField(
            event, Quartz.kCGEventSourceStateID
        )
        return source_state_id != Quartz.kCGEventSourceStateHIDSystemState

    def register_event(self, event_type, modifier_text, keycode):
        key_name = self.config.get_key_name(keycode)
        text = ""

        if event_type == Quartz.kCGEventKeyDown:
            text = f"🟢 Key Pressed: {modifier_text} {key_name} (Keycode: {keycode})".strip()
            data = {
                "type": "KEY_DOWN",
                "key": key_name,
                "modifiers": modifier_text,
                "keycode": keycode,
            }
            self.data_queue.put(data)
            self.log(text)
        elif event_type == Quartz.kCGEventKeyUp:
            text = f"🔴 Key Released: {modifier_text} {key_name} (Keycode: {keycode})".strip()
            data = {
                "type": "KEY_UP",
                "key": key_name,
                "modifiers": modifier_text,
                "keycode": keycode,
            }
            self.data_queue.put(data)
            self.log(text)
        elif event_type == "KEY_HOLD":
            text = f"🕒 Key Hold: {modifier_text} (Keycode: {keycode})".strip()
            data = {
                "type": "KEY_HOLD",
                "key": key_name,
                "modifiers": modifier_text,
                "keycode": keycode,
            }
            self.data_queue.put(data)
            self.log(text)
        elif event_type == EventsEnum.KEY_HOLD_RELEASE:
            text = f"🕒 Key Hold Released: {modifier_text} (Keycode: {keycode})".strip()
            data = {
                "type": "KEY_HOLD_RELEASE",
                "key": key_name,
                "modifiers": modifier_text,
                "keycode": keycode,
            }
            self.data_queue.put(data)
            self.log(text)

    def start_key_logger_threaded(self):
        self.log("Waiting for event to start keylogger")
        self.start_event.wait(None)
        self.log("Starting keylogger")
        self.start_keylogger()

    def start_keylogger(self):
        # Create an event tap to intercept keyboard events
        event_tap = Quartz.CGEventTapCreate(
            Quartz.kCGSessionEventTap,
            Quartz.kCGHeadInsertEventTap,
            0,
            (1 << Quartz.kCGEventKeyDown)
            | (1 << Quartz.kCGEventKeyUp)
            | (1 << Quartz.kCGEventFlagsChanged),
            self.keyboard_callback,
            self,
        )

        if not event_tap:
            self.log(
                "❌ Failed to create event tap. Ensure accessibility permissions are enabled."
            )
            exit(1)

        # Add the event tap to the run loop
        run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, event_tap, 0)
        Quartz.CFRunLoopAddSource(
            Quartz.CFRunLoopGetCurrent(), run_loop_source, Quartz.kCFRunLoopCommonModes
        )

        self.log(
            "🎹 Key Logger Active (Press any key to see its keycode). Press Ctrl+C to stop."
        )

        run_loop_ref = Quartz.CFRunLoopGetCurrent()

        # Create a repeating timer that fires every 3 seconds
        timer = Quartz.CFRunLoopTimerCreate(
            None,  # Default allocator
            1.0,  # Fire after 3 seconds
            1.0,  # Repeat every 3 seconds
            0,  # Flags (usually 0)
            0,  # Priority/order (usually 0)
            self.check_stop_loop,  # Correct function signature (timer, info)
            self,  # Context (not needed, so None)
        )

        # Add the timer to the run loop
        Quartz.CFRunLoopAddTimer(run_loop_ref, timer, Quartz.kCFRunLoopDefaultMode)

        result = Quartz.CFRunLoopRun()  # Keep the loop running
        self.log("🛑 Key Logger Stopped")

    def set_mouse_position(self, x, y):
        """Moves the mouse cursor to (x, y) and generates an event."""
        event = Quartz.CGEventCreateMouseEvent(
            None,  # No special source
            Quartz.kCGEventMouseMoved,
            (x, y),
            Quartz.kCGMouseButtonLeft,  # Button is required but not used for movement
        )
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

    def set_mouse_x(self, x):
        """Sets only the X position while keeping Y unchanged."""
        (_, current_y) = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
        Quartz.CGWarpMouseCursorPosition((x, current_y))

    def set_mouse_y(self, y):
        """Sets only the Y position while keeping X unchanged."""
        (current_x, _) = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
        Quartz.CGWarpMouseCursorPosition((current_x, y))

    def inc_mouse_x(self, x_delta):
        """Sets only the X position while keeping Y unchanged."""
        (current_x, current_y) = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
        Quartz.CGWarpMouseCursorPosition((current_x + x_delta, current_y))

    def inc_mouse_y(self, y_inc):
        """Sets only the Y position while keeping X unchanged."""
        (current_x, current_y) = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
        Quartz.CGWarpMouseCursorPosition((current_x, current_y + y_inc))


if __name__ == "__main__":
    config = custom_config
    key_logger = KeyLogger(config)
    key_logger.start_keylogger()
