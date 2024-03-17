#!/bin/bash

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICON="${SCRIPT_DIR}/icons/icons8-sun.svg"

if [[ "$1" == "up" ]] then
  brightness="$(brightnessctl s +5% | grep -Eo '[0-9]{1,3}%')"
elif [[ "$1" == "down" ]]; then
  brightness="$(brightnessctl s 5%- | grep -Eo '[0-9]{1,3}%')"
else
  brightness="$(brightnessctl | grep -Eo '[0-9]{1,3}%')"
fi

brightness=${brightness%%%}

dunstify -t 2000 -i "${ICON}" -h string:x-canonical-private-synchronous:brightness "${brightness}%" -h int:value:${brightness}
