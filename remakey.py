import time
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QScrollArea,
)
from PyQt6.QtCore import QTimer
import sys
from key_logger import KeyLogger
from custom_layers import custom_config

import queue
import threading

# Keylogger initialization and definition
key_logger = KeyLogger(custom_config)
data_queue = key_logger.data_queue
change_layer_queue = key_logger.change_layer_queue
start_event = key_logger.start_event
stop_event = key_logger.stop_event
start_keylogger = key_logger.start_key_logger_threaded
thread = threading.Thread(target=start_keylogger, daemon=True)

# Define data fetching timers
is_live_logs_enabled = True
clock_display_timer = QTimer()
log_fetcher_timer = QTimer()
change_layer_timer = QTimer()

# Define components
app = QApplication(sys.argv)
widget = QWidget()
layout = QVBoxLayout()
button = QPushButton("Start")
scroll_widget = QWidget()
scroll_layout = QVBoxLayout()
scroll_area = QScrollArea()
clear_button = QPushButton("Clear")
start = QPushButton("Stop")
clock_display_label = QLabel("Hello")
live_logs_toggle = QPushButton("Toggle Live Logs")
live_logs_toggle.setCheckable(True)
live_logs_toggle.setChecked(True)
current_layer_label = QLabel(f"Current Layer: 0")

# Set layout
layout.addWidget(button)
layout.addWidget(start)
layout.addWidget(clock_display_label)
layout.addWidget(current_layer_label)
layout.addWidget(live_logs_toggle)
widget.setLayout(layout)
scroll_widget.setLayout(scroll_layout)
scroll_area.setWidgetResizable(True)
scroll_area.setMinimumHeight(300)
scroll_area.setMinimumWidth(300)
scroll_area.setMaximumHeight(300)
scroll_area.setWidget(scroll_widget)
layout.addWidget(scroll_area)
layout.addWidget(clear_button)

# Ui and timers handlers
def appendLabel():
    try:
        while data_queue.not_empty:
            text = data_queue.get(False)
            if text.startswith("🔄 Switched to Layer "):
                current_layer_label.setText(text)

            if text is None or text == "":
                return
            newText = QLabel(text)
            scroll_layout.addWidget(newText)
            scroll_area.verticalScrollBar().setValue(
                scroll_area.verticalScrollBar().maximum()
            )
    except queue.Empty:
        pass


def clear_scroll_layout():
    """Function to remove all items from the scroll layout."""
    while scroll_layout.count():
        item = scroll_layout.takeAt(0)  # Get the first item
        widget = item.widget()
        if widget:
            widget.deleteLater()  # Properly delete widget

    # Reset scroll bar to the top
    scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().minimum())


def clear_data_queue():
    while not data_queue.empty():
        data_queue.get()


def changedLayerLabelUpdater():
    try:
        while change_layer_queue.not_empty:
            text = change_layer_queue.get(False)
            current_layer_label.setText(f"🔄 Switched to Layer {text}")
    except queue.Empty:
        pass


def live_logs_toggle_clicked():
    (
        log_fetcher_timer.stop()
        if log_fetcher_timer.isActive()
        else log_fetcher_timer.start(100)
    )
    clear_data_queue()

# Connect Ui and timers handlers
clear_button.clicked.connect(lambda: clear_scroll_layout())
clock_display_timer.timeout.connect(
    lambda: clock_display_label.setText(time.strftime("%Y-%m-%d %H:%M:%S"))
)
log_fetcher_timer.timeout.connect(lambda: appendLabel())
button.clicked.connect(lambda: start_event.set())
start.clicked.connect(lambda: stop_event.set())
live_logs_toggle.clicked.connect(lambda: live_logs_toggle_clicked())
change_layer_timer.timeout.connect(lambda: changedLayerLabelUpdater())


thread.start()
widget.show()
clock_display_timer.start(100)
change_layer_timer.start(100)
log_fetcher_timer.start(100)
sys.exit(app.exec())
thread.join()
