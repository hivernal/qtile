#!/bin/bash

dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP=wlroots
systemctl --user stop pipewire wireplumber xdg-desktop-portal xdg-desktop-portal-hyprland
systemctl --user start wireplumber
/usr/lib/polkit-kde-authentication-agent-1 &
