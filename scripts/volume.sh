#!/bin/bash

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ICONS_DIR="${SCRIPT_DIR}/icons"

if [[ "$1" == "up" ]] then
  pactl set-sink-volume @DEFAULT_SINK@ +5%
elif [[ "$1" == "down" ]]; then
  pactl set-sink-volume @DEFAULT_SINK@ -5%
elif [[ "$1"  == "mute" ]]; then
  pactl set-sink-mute @DEFAULT_SINK@ toggle
fi

muted="$(pactl get-sink-mute @DEFAULT_SINK@ | cut -d " "  -f2)"
volume="$(pactl get-sink-volume @DEFAULT_SINK@ | awk '(NR == 1) {print $5}')"
volume=${volume%%%}
if [[ ${muted} == "yes" ]]; then
    icon=audio-volume-muted-panel.svg
else
  if (( ${volume} == 0 )); then
    icon=audio-volume-zero-panel.svg
  elif (( ${volume} <= 20 )); then
    icon=audio-volume-low-panel.svg
  elif (( ${volume} <= 50 )); then
    icon=audio-volume-medium-panel.svg
  else
    icon=audio-volume-high-panel.svg
  fi
fi

dunstify -t 2000 -i "${ICONS_DIR}/${icon}" -h string:x-canonical-private-synchronous:audio "${volume}%" -h int:value:${volume}
