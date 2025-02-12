import asyncio
from enums import KeyNames
from key_logger import KeyLogger
from custom_layers import custom_config
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

    def get_change_layer_logs(self):
        logs = []
        while self.change_layer_queue.not_empty:
            text = self.change_layer_queue.get(False)
            logs.append(text)
        return logs

    async def get_change_layer_logs_generator(self):
        while True:
            if not self.change_layer_queue.empty():
                change_layer = self.change_layer_queue.get(block=False)
                text = f"id:layer_changed_{change_layer}\nevent: layerChange\ndata: {change_layer}\n\n"
                yield text
            if not self.data_queue.empty():
                log = self.data_queue.get(block=False)
                text = f"id:123\nevent: log\ndata: {log}\n\n"
                yield text

            await asyncio.sleep(0.1)

    def clear_logs(self):
        while not self.data_queue.empty():
            self.data_queue.get()

    def clear_change_layer_logs(self):
        while not self.change_layer_queue.empty():
            self.change_layer_queue.get()

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

    def get_current_layer_mapping(self):
        layer_id = self.key_logger.config.layers[
            self.key_logger.config.current_layer
        ].id
        return self.get_layer_mapping(layer_id)

    def get_current_layer(self):
        layer_id = self.key_logger.config.layers[
            self.key_logger.config.current_layer
        ].id
        return self.get_layer(layer_id)

    def set_current_layer_by_id(self, layer_id: int):
        self.key_logger.set_layer_by_id(layer_id)

    def add_remap_to_layer(self, layer_id: int, key: KeyNames, value: KeyNames):
        self.key_logger.config.add_remap_to_layer(layer_id, key, value)
