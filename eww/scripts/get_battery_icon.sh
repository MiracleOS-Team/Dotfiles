#!/bin/sh

# Get the battery information
BATTERY=$(upower -e | grep 'BAT' | head -n 1)

# Ensure BATTERY is not empty
if [ -z "$BATTERY" ]; then
    echo "battery-missing-symbolic"
    exit 0
fi

# Extract battery details
STATE=$(upower -i "$BATTERY" | grep -E "state" | awk '{print $2}')
CHARGE=$(upower -i "$BATTERY" | grep -E "percentage" | awk '{print $2}' | tr -d '%')

# Ensure CHARGE is numeric
if ! [[ "$CHARGE" =~ ^[0-9]+$ ]]; then
    echo "battery-missing-symbolic"
    exit 0
fi

# Determine GTK3 symbolic icon
if [ "$STATE" == "fully-charged" ]; then
    ICON="battery-full-charged-symbolic"
elif [ "$STATE" == "charging" ]; then
    if [ "$CHARGE" -ge 90 ]; then
        ICON="battery-full-charging-symbolic"
    elif [ "$CHARGE" -ge 70 ]; then
        ICON="battery-good-charging-symbolic"
    elif [ "$CHARGE" -ge 40 ]; then
        ICON="battery-low-charging-symbolic"
    elif [ "$CHARGE" -ge 10 ]; then
        ICON="battery-caution-charging-symbolic"
    else
        ICON="battery-empty-charging-symbolic"
    fi
elif [ "$STATE" == "discharging" ]; then
    if [ "$CHARGE" -ge 90 ]; then
        ICON="battery-full-symbolic"
    elif [ "$CHARGE" -ge 70 ]; then
        ICON="battery-good-symbolic"
    elif [ "$CHARGE" -ge 40 ]; then
        ICON="battery-low-symbolic"
    elif [ "$CHARGE" -ge 10 ]; then
        ICON="battery-caution-symbolic"
    else
        ICON="battery-empty-symbolic"
    fi
else
    ICON="battery-missing-symbolic"
fi

# Output the GTK3 icon name
echo "$ICON"
