#!/bin/bash

# Initialize variable to hold the final icon
ICON=""

# Check for active connections (wired, wireless, or WWAN)
ACTIVE_CONNECTIONS=$(nmcli -t -f TYPE,STATE device status | grep 'connected')

# Check if there are any active connections
if [ -z "$ACTIVE_CONNECTIONS" ]; then
    ICON="network-offline-symbolic"
else
    # Iterate through each active connection and prioritize
    while IFS=: read -r TYPE STATE; do
        case "$TYPE" in
            ethernet)
                # Ethernet connection: High priority
                ICON="network-wired-symbolic"
                break
                ;;
            wifi)
                # Wi-Fi connection: Check signal strength
                SIGNAL=$(nmcli -t -f IN-USE,SIGNAL device wifi | grep '*' | awk -F: '{print $2}')
                if [[ "$SIGNAL" =~ ^[0-9]+$ ]]; then
                    if [ "$SIGNAL" -ge 75 ]; then
                        ICON="network-wireless-signal-excellent-symbolic"
                    elif [ "$SIGNAL" -ge 50 ]; then
                        ICON="network-wireless-signal-good-symbolic"
                    elif [ "$SIGNAL" -ge 25 ]; then
                        ICON="network-wireless-signal-ok-symbolic"
                    else
                        ICON="network-wireless-signal-weak-symbolic"
                    fi
                else
                    ICON="network-wireless-signal-none-symbolic"
                fi
                break
                ;;
            wwan)
                # WWAN connection: Check signal strength
                SIGNAL=$(nmcli -t -f TYPE,SIGNAL device status | grep 'wwan' | awk -F: '{print $2}')
                if [[ "$SIGNAL" =~ ^[0-9]+$ ]]; then
                    if [ "$SIGNAL" -ge 75 ]; then
                        ICON="network-cellular-signal-excellent-symbolic"
                    elif [ "$SIGNAL" -ge 50 ]; then
                        ICON="network-cellular-signal-good-symbolic"
                    elif [ "$SIGNAL" -ge 25 ]; then
                        ICON="network-cellular-signal-ok-symbolic"
                    else
                        ICON="network-cellular-signal-weak-symbolic"
                    fi
                else
                    ICON="network-cellular-signal-none-symbolic"
                fi
                break
                ;;
            *)
                # Fallback for unknown connection types
                ICON="network-offline-symbolic"
                break
                ;;
        esac
    done <<< "$ACTIVE_CONNECTIONS"
fi

# Output the final GTK3 icon name
echo "$ICON"
