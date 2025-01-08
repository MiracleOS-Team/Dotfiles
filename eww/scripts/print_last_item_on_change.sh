#!/bin/bash

# Check if a filename is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <file>"
  exit 1
fi

FILE=$1

# Ensure the file exists
if [ ! -f "$FILE" ]; then
  echo "File not found!"
  exit 1
fi

echo ""
echo ""

# Monitor the file for changes and suppress inotifywait messages
inotifywait -m -e modify --format "%w%f" "$FILE" 2>/dev/null | while read -r changed_file; do
 
    python3.11 scripts/take_last_item_wc.py "$changed_file"
    sleep 4
    echo ""
    

done
