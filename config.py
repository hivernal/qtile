# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.backend.wayland import InputConfig
import os
import subprocess

if qtile.core.name == "x11":
    terminal = "st tmux"
    app_launcher = "dmenu_run"
    script = os.path.expanduser("~/.config/qtile/scripts/xorg_autostart.sh")
    screenshot = "flameshot gui"
elif qtile.core.name == "wayland":
    terminal = "foot"
    app_launcher = "bemenu-run"
    screenshot = os.path.expanduser("~/.config/qtile/scripts/screenshot.sh")
    script = os.path.expanduser("~/.config/qtile/scripts/wayland_autostart.sh")

@hook.subscribe.startup_once
def autostart():
    subprocess.run([script])

wl_input_rules = {
    "type:touchpad": InputConfig(natural_scroll=True, tap=True,
                                 pointer_accel=0.3),
    "type:keyboard": InputConfig(kb_options="grp:win_space_toggle",
                                 kb_repeat_rate=25, kb_repeat_delay=300,
                                 kb_layout="us,ru"),
}

mod = "mod4"
volume = os.path.expanduser("~/.config/qtile/scripts/volume.sh ")
brightness = os.path.expanduser("~/.config/qtile/scripts/brightness.sh ")
home = os.path.expanduser("~/")

keys = [
    Key([mod], "l", lazy.layout.grow_main(), desc="Move focus to left"),
    Key([mod], "h", lazy.layout.shrink_main(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "return", lazy.layout.swap_main()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "shift"], "q", lazy.spawn("systemctl poweroff"), desc="Shutdown Qtile"),
    Key([mod], "p", lazy.spawn(app_launcher), desc="Dmenu"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(volume + "up")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(volume + "down")),
    Key([], "XF86AudioMute", lazy.spawn(volume + "mute")),
    Key([], "XF86MonBrightnessUp", lazy.spawn(brightness + "up")),
    Key([], "XF86MonBrightnessDown", lazy.spawn(brightness + "down")),
    Key([mod], "s", lazy.spawn(screenshot)),
    Key([], "Print", lazy.spawn(screenshot)),
    Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),

]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            Key([mod],i.name,lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name)),
            Key([mod, "shift"],i.name,lazy.window.togroup(i.name),
                desc="Switch to & move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(border_focus="#d2d9f8", border_normal="#5e5f67",
                     border_width=3, ratio=0.55,
                     new_client_position='before_current'),
    layout.Max(border_focus="#d2d9f8", border_normal="#5e5f67", border_width=3),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font ExtraBold",
    fontsize=16,
    background="#1a1b26",
    foreground="#d2d9f8",
    padding=0,
    margin=0,
)
extension_defaults = widget_defaults.copy()

import mywidgets

@lazy.function
def get_number_of_windows(qtile):
	return len(qtile.currentGroup.windows)

screens = [
    Screen(
        wallpaper="~/pictures/groot-dark.png",
        wallpaper_mode="stretch",
        top=bar.Bar(
            [
                widget.GroupBox(highlight_method="block", active="#d2d9f8",
                                inactive="#5e5f67",
                                block_highlight_text_color="#d2d9f8",
                                this_screen_border="#5e5f67",
                                this_current_screen_border="#5e5f67",
                                margin_y=5, padding=10),
                mywidgets.CurrentLayout(fmt="{} "),
                widget.WindowName(max_chars=70),
                widget.KeyboardLayout(configured_keyboards=["us", "ru,us"],
                                      display_map={"us": "us", "ru,us": "ru"},
                                      fmt="KEY {}"),
                widget.TextBox(" | "),
                widget.Volume(fmt="VOL {}", update_interval=1),
                widget.TextBox(" | "),
                widget.Memory(format="MEM {MemUsed:.0f}M", update_interval=2),
                widget.TextBox(" | "),
                widget.Battery(format="BAT {percent:2.0%}"),
                widget.TextBox(" | "),
                widget.Wlan(format="NET {essid}", interface="wlo1",
                            update_interval=5),
                widget.TextBox(" | "),
                widget.Clock(format="%H:%M", update_interval=30),
                widget.TextBox()
                # widget.KeyboardLayout(configured_keyboards=["us", "ru"],
                #                       display_map={"us": "us", "ru": "ru"},
                #                       fmt="<span font_size='16pt' letter_spacing='20000'>󰌌</span><span rise='2700'>{}</span>"),
                # widget.TextBox(padding=10),
                # MyVolume(emoji_list=["󰕿", "󰖀", "󰖀", "󰕾"], emoji=True),
                # widget.TextBox(padding=10),
                # widget.Memory(format="<span font_size='16pt' letter_spacing='1000'> </span>{MemUsed:.0f}M", interface="wlo1"),
                # widget.TextBox(padding=10),
                # widget.BatteryIcon(theme_path="/usr/share/icons/Qogir-dark"),
                # widget.Battery(format="{percent:2.0%}"),
                # widget.TextBox(padding=10),
                # widget.Wlan(format="<span font_size='15pt' letter_spacing='-1000' rise='-1500'>󰣺 </span>{essid}", interface="wlo1"),
                # widget.TextBox(padding=10),
                # widget.Clock(format="<span font_size='16pt' letter_spacing='20000'></span><span rise='2000'>%H:%M</span>"),
                # widget.TextBox(),
            ],
            26,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus="#d2d9f8", border_normal="#5e5f67",
    border_width=3,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
# wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
