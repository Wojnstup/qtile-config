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

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess
import os

mod = "mod4"
mod_l = "mod1"
terminal = guess_terminal()


keys = [
    # Switch between windows
    Key([mod], "j", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "o", lazy.spawn('rofi -combi-modi window,drun,ssh -theme solarized -font "hack 15" -show combi'), 
        desc="Spawn a command using a prompt widget"),
    Key([mod], "b", lazy.hide_show_bar("top")),
    Key([mod], "t", lazy.window.toggle_floating()),

    # Open apps
    Key([mod_l], "s", lazy.spawn("steam")),
    Key([mod_l], "d", lazy.spawn("discord")),
    Key([mod_l], "f", lazy.spawn("firefox")),
    Key([mod_l], "m", lazy.spawn("spotify")),
    Key([mod_l], "p", lazy.spawn("pcmanfm")),
    
    # Take a screenshot
    Key([mod, "shift"], "s", lazy.spawn("python3 /home/wojnstup/.config/qtile/screenshot.py"))#function(take_screenshot))
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=False),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Columns(border_focus='#8c1bdb', margin=7),
    layout.Max(border_focus='#8c1bdb', margin=5),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=ddd
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=13,
    padding=3,
)
extension_defaults = widget_defaults.copy()


### VOLUME WIDGET ###
def get_volume():
    #amixer -c 0 get Master
    subprocess.check_output("amixer", "-c", "0", "get", "Master")

def add_volume():
    #amixer -c 0 set Master 5%+
    subprocess.check_output(["amixer", "-c", "0", "set", "Master", "5%+"])

def lower_volume():
    subprocess.check_output(["amixer", "-c", "0", "set", "Master", "5%-"])

custom_font = "Terminus"

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active="#8b3eee",
                    borderwidth=0,
                    block_highlight_text_color="#B939EC",
                    disable_drag=True,
                    margin_x=5,
                    font= custom_font,
                    fontsize = 10
                    ),
                widget.WindowName(
                    foreground="#B939EC",
                    font = custom_font,
                    fontsize = 15
                    ),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Notify(
                    foreground="#dd6ffb",  
                    font = custom_font,
                    fontsize = 15,
                    audiofile="/home/wojnstup/Music/notification.mp3"
                    ),
                widget.TextBox(text="/", fontsize=20, foreground="#600eb6"),
                widget.Net(
                    foreground="#8b3eee",
                    fontsize = 15,
                    font = custom_font,
                    format='{down} ↓↑ {up}'
                    ),
                widget.TextBox(text="/", fontsize=20, foreground="#600eb6"),
                widget.CPU(
                    fontsize = 15,
                    font = custom_font,
                    foreground="#B939EC"
                    ),
                widget.TextBox(text="/", fontsize=20, foreground="#600eb6"),
                widget.Memory(
                    fontsize = 15,
                    font = custom_font,
                    foreground="#8b3eee"
                    ),
                widget.TextBox(text="/", fontsize=20, foreground="#600eb6"),
                widget.TextBox(
                    font = custom_font,
                    text="🔊",
                    foreground="#B939EC",
                    mouse_callbacks={
                        "Button4" : add_volume,
                        "Button5" : lower_volume
                        },
                    fontsize = 15
                ),
                widget.TextBox(text="/", fontsize=20, foreground="#600eb6"),
                widget.Clock(
                    fontsize = 15,
                    font = custom_font,
                    format=' %I:%M %p', 
                    foreground="#8b3eee"
                    ),
                widget.TextBox(text="/", fontsize=20, foreground="#600eb6"),
                widget.QuickExit(
                    foreground="#B939EC", 
                    default_text="&#x23FB;",
                    fontsize = 20
                    )
            ],
            24,
            background= "#151515"
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
