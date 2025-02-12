#!/bin/bash

APP_PATH="$HOME/Desktop/remakey/remakey/templates/electron_main.js"

# Get the PID of the main Electron process (excluding helper processes)
ELECTRON_PID=$(pgrep -f "[e]lectron $APP_PATH")

if [ -n "$ELECTRON_PID" ]; then
    echo "Electron is running (PID: $ELECTRON_PID), closing it..."
    kill "$ELECTRON_PID"
    sleep 2  # Wait to ensure it stops
else
    # Launch Electron
    echo "Starting Electron..."
    electron "$APP_PATH" &
fi


