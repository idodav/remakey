import Quartz
import threading
import queue
from enums import MODIFIER_KEY_TO_BITMASK, MODIFIERS, KeyNames
from custom_layers import custom_config
import time
from remap_layer import ActionsEnum, Config, KeyActionConfiguration


class KeyLogger:
    def __init__(self, config: Config):
        self.start_event = threading.Event()
        self.stop_event = threading.Event()
        self.data_queue = queue.Queue()
        self.change_layer_queue = queue.Queue()
        self.config: Config = config
        self.is_silent = self.config.is_silent

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

    def send_key_event(self, keycode, event_type):
        """Send a new keyboard event with the specified keycode."""
        event = Quartz.CGEventCreateKeyboardEvent(
            None, keycode, event_type == Quartz.kCGEventKeyDown
        )
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

    def get_active_modifiers(self, flags):
        """Get active modifier keys as a list."""
        return [name for bitmask, name in MODIFIERS.items() if flags & bitmask]

    def rotate_layer(self):
        self.config.rotate_current_layers()
        self.log(f"🔄 Switched to Layer {self.config.current_layer}")
        self.data_queue.put(f"🔄 Switched to Layer {self.config.current_layer}")
        self.change_layer_queue.put(self.config.current_layer)

    def set_layer(self, layer_index):
        self.config.set_current_layer(layer_index)
        self.log(f"🔄 Switched to Layer {self.config.current_layer}")
        self.data_queue.put(f"🔄 Switched to Layer {self.config.current_layer}")
        self.change_layer_queue.put(self.config.current_layer)

    @staticmethod
    def keyboard_callback(proxy, event_type, event, refcon):
        """Callback function to log key presses with keycodes."""
        self_instance: KeyLogger = refcon
        keycode = Quartz.CGEventGetIntegerValueField(
            event, Quartz.kCGKeyboardEventKeycode
        )
        flags = Quartz.CGEventGetFlags(event)
        active_modifiers = self_instance.get_active_modifiers(flags)
        suppress_event = False

        if event_type == Quartz.kCGEventFlagsChanged:
            keycode_modifier_flag = MODIFIER_KEY_TO_BITMASK[KeyNames(keycode)]
            generated_event = (
                Quartz.kCGEventKeyDown
                if keycode_modifier_flag & flags
                else Quartz.kCGEventKeyUp
            )

            if generated_event == Quartz.kCGEventKeyDown:
                self_instance.handle_key_down(keycode, generated_event)
            else:
                self_instance.register_event(generated_event, active_modifiers, keycode)

        elif event_type == Quartz.kCGEventKeyDown:
            self_instance.register_event(event_type, active_modifiers, keycode)
            suppress_event = self_instance.handle_key_down(keycode, event_type)
        elif event_type == Quartz.kCGEventKeyUp:
            self_instance.register_event(event_type, active_modifiers, keycode)
        if self_instance.config.suppress_original:
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
        self.data_queue.put(
            f"Active modifiers: {active_modifiers} (Keycode: {keycode})".strip()
        )

    def handle_key_down(self, keycode, event_type):
        if keycode == self.config.change_layer_key.value:
            self.rotate_layer()
            return True  # Suppress original key
        elif self.config.check_key_in_mapping(keycode):
            action: KeyActionConfiguration = self.config.get_key_action(keycode)
            action_type = action.get("type")
            action_value = action.get("value")

            # Default action is remapping
            if action_type is None:
                new_keycode = self.config.get_remapped_value(keycode)
                if new_keycode is not None:
                    self.log(
                        f"🔁 Remapping {KeyNames(keycode).name} → {KeyNames(new_keycode).name}"
                    )
                    self.data_queue.put(
                        f"🔁 Remapping {KeyNames(keycode).name} → {KeyNames(new_keycode).name}"
                    )

                    self.send_key_event(new_keycode, event_type)
                    return True  # Suppress original key
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
        return False

    def register_event(self, event_type, modifier_text, keycode):
        key_name = self.config.get_key_name(keycode)
        text = ""

        if event_type == Quartz.kCGEventKeyDown:
            text = f"🟢 Key Pressed: {modifier_text} {key_name} (Keycode: {keycode})".strip()
            self.data_queue.put(text)
            self.log(text)
        elif event_type == Quartz.kCGEventKeyUp:
            text = f"🔴 Key Released: {modifier_text} {key_name} (Keycode: {keycode})".strip()
            self.data_queue.put(text)
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
