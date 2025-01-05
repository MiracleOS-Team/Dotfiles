#!/bin/bash

# Check if a widget name is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <widget_name>"
    exit 1
fi

# Name of the widget to toggle
WIDGET_NAME="$1"

# Check if the widget is active
if eww active-windows | grep -q "\b$WIDGET_NAME\b"; then
    # Close the widget if it is active
    eww close "$WIDGET_NAME"
    echo "Closed widget: $WIDGET_NAME"
else
    # Open the widget if it is not active
    eww open "$WIDGET_NAME"
    echo "Opened widget: $WIDGET_NAME"
fi
