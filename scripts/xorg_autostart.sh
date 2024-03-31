#!/bin/bash

picom -b --config /dev/null --backend glx --glx-no-stencil --glx-no-rebind-pixmap --vsync --no-frame-pacing --no-fading-openclose --no-fading-destroyed-argb --use-ewmh-active-win
/usr/lib/polkit-kde-authentication-agent-1 &
