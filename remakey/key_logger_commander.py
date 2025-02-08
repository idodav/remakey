from remakey.enums import KeyNames
from key_logger import KeyLogger
from remakey.custom_layers import custom_config
import threading


class KeyLoggerManager:
    def __init__(self):
        self.key_logger = KeyLogger(custom_config)
        self.data_queue = self.key_logger.data_queue
        self.change_layer_queue = self.key_logger.change_layer_queue
        self.start_event = self.key_logger.start_event
        self.stop_event = self.key_logger.stop_event
        self.start_keylogger = self.key_logger.start_key_logger_threaded
        self.thread = threading.Thread(target=self.start_keylogger, daemon=True)

    def start_thread(self):
        self.thread.start()

    def start(self):
        self.start_event.set()

    def stop(self):
        self.stop_event.set()

    def get_logs(self):
        logs = []
        while self.data_queue.not_empty:
            text = self.data_queue.get(False)
            logs.append(text)
        return logs

    def clear_logs(self):
        while not self.data_queue.empty():
            self.data_queue.get()

    def join_thread(self):
        self.thread.join()

    def get_layer_names(self):
        return self.key_logger.config.get_layer_names()

    def get_layer_ids(self):
        return self.key_logger.config.get_layer_ids()

    def get_layers(self):
        return self.key_logger.config.layers

    def get_layer(self, layer_id: str):
        return self.key_logger.config.get_layer(layer_id)

    def get_layer_mapping(self, layer_id: str):
        layer = self.key_logger.config.get_layer(layer_id)
        mapping = layer.mapping.get("mapping")
        return mapping

    def set_current_layer_by_id(self, layer_id: int):
        self.key_logger.config.set_current_layer_by_id(layer_id)

    def add_remap_to_layer(self, layer_id: int, key: KeyNames, value: KeyNames):
        self.key_logger.config.add_remap_to_layer(layer_id, key, value)
