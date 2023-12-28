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

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess

mod = "mod4"
terminal = "kitty"


# navigation_mode bisa "vim" ataupun "regular"
navigation_mode = "vim"
# system_control_mode bisa "fn" ataupun "custom"
system_control_mode = "custom"

# pc_mode "laptop" atau "desktop"
pc_mode = "desktop"



if navigation_mode == "vim":
    navigation_keys = ["h", "j", "k", "l"]
elif navigation_mode == "regular":
    navigation_keys = ["Left", "Down", "Up", "Right"]



if system_control_mode == "fn":
    keys = [
        # audio control
        Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 2%+"),
            desc="Raise volume by 2%"),
        Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 2%-"),
            desc="Reduce volume by 2%"),
        Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle"),
            desc="Mute audio"),

        # brightness control
        Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%"),
            desc="Raise brightness"),
        Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5-%"),
            desc="Reduce brightness"),

    ]
elif system_control_mode == "custom":
    keys = [
        # audio control
        Key([mod, "control"], "0", lazy.spawn("amixer -q set Master 2%+"),
            desc="Raise volume by 2%"),
        Key([mod, "control"], "9", lazy.spawn("amixer -q set Master 2%-"),
            desc="Reduce volume by 2%"),
        Key([mod, "control"], "8", lazy.spawn("amixer set Master toggle"),
            desc="Mute audio"),

        # brightness control
        Key([mod, "control"], "6", lazy.spawn("brightnessctl set +5%"),
            desc="Raise brightness"),
        Key([mod, "control"], "5", lazy.spawn("brightnessctl set 5-%"),
            desc="Reduce brightness"),

    ]


# main keybindings
keys.extend([

    # Switch between windows
    Key([mod], navigation_keys[0], lazy.layout.left(),
        desc="Move focus to left"),
    Key([mod], navigation_keys[3], lazy.layout.right(),
        desc="Move focus to right"),
    Key([mod], navigation_keys[1], lazy.layout.down(),
        desc="Move focus down"),
    Key([mod], navigation_keys[2], lazy.layout.up(),
        desc="Move focus up"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], navigation_keys[0], lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], navigation_keys[3], lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], navigation_keys[1], lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], navigation_keys[2], lazy.layout.shuffle_up(),
        desc="Move window up"),

    # MonadTall Layout specific controls
    Key([mod], "space", lazy.layout.flip(),
       desc="Flip master postion"),
    Key([mod], "i", lazy.layout.grow(),
       desc="Increase window size"),
    Key([mod], "m", lazy.layout.shrink(),
       desc="Reduce window size"),



    Key([mod], "n", lazy.layout.reset(),
        desc="Reset all window sizes"),
    Key([mod, "shift"], "m", lazy.layout.maximize(),
        desc="Toggle a window between minimum and maximum sizes"),


    # floating & fullscreen
    Key([mod, "shift"], "space", lazy.window.toggle_floating(),
        desc="Toggle floating window"),
    Key([mod, "control"], "space", lazy.window.toggle_fullscreen(),
        desc="Toggle floating window"),


    # Switch focus to specific monitor (out of three)
    Key([mod, "control"], "1", lazy.to_screen(0),
        desc='Keyboard focus to monitor 1'),
    Key([mod, "control"], "2", lazy.to_screen(1),
        desc='Keyboard focus to monitor 2'),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(),
        desc="Toggle between layouts"),
    Key([mod, "shift"], "Tab", lazy.prev_layout(),
        desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(),
        desc="Kill focused window"),



    Key([mod, "control"], "r", lazy.restart(),
        desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(),
        desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),



    # Launch application
    Key([mod], "Return", lazy.spawn(terminal),
        desc="Launch terminal"),
    Key([mod], "f", lazy.spawn("kitty -e ranger"),
        desc="Launch file manager"),
    Key([mod, "shift"], "f", lazy.spawn("thunar"),
        desc="Launch alternative file manager"),
    Key([mod], "b", lazy.spawn("brave-browser"),
        desc="Launch main browser"),
    Key([mod, "shift"], "b", lazy.spawn("firefox"),
        desc="Launch alternative browser"),
    Key([mod], "d", lazy.spawn("rofi -modi drun -show drun -show-icons -theme dmenu by Qball"),
        desc="Launch Rofi with .desktop"),
    Key([mod, "shift"], "d", lazy.spawn("rofi -modi run -show run -theme dmenu by Qball"),
        desc="Launch Rofi with run command"),
    Key([], "Print", lazy.spawn("xfce4-screenshooter"),
        desc="Launch Rofi with run command"),

    # screenlock
    Key([mod], "Escape", lazy.spawn("i3lock-fancy"),
        desc="screenlock")

])


all_workspaces = "123456789"
groups = [Group(i) for i in all_workspaces]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])


# layout settings
gap_width = 10
border_w = 2
focus_color = "#F085F7"
infocus_color = "#000000"
general_layout_setting = {
    "border_focus": focus_color,
    "border_normal": infocus_color,
    "border_width": border_w,
    "margin": gap_width
}


# list of window layouts
layouts = [
    layout.MonadTall(
        single_margin = gap_width,
        new_client_position = 'top',
        add_on_top = True,
        **general_layout_setting
        ),
    layout.MonadWide(
        single_margin = gap_width,
        new_client_position = 'top',
        add_on_top = True,
        **general_layout_setting
        ),
    layout.Max(),
    layout.RatioTile(
        **general_layout_setting
    ),
    #layout.Spiral(
	#	main_pane = 'left',
	#	ratio = 0.5,
	#	**general_layout_setting
	#	),
]


# widget settings
widget_defaults = dict(
    font = "Dejavu Sans",
    fontsize = 12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# widget_color
background_highlight_workspace = "#000000"
highlight_workspace = focus_color
unhighlight_workspace = "#7f7f7f"
dark_highlight_workspace = "#9f9f9f"

# separator and space settings
space_width = 7
separator_line = 2


# widget on the left
left_widgets = [
    widget.GroupBox(
        visible_groups = all_workspaces,
        hide_unused = False,
        inactive = unhighlight_workspace,
        highlight_method = 'border',
        this_current_screen_border = [highlight_workspace]*2,
        this_screen_border = [dark_highlight_workspace]*2,
        other_current_screen_border = [highlight_workspace]*2,
        other_screen_border = [dark_highlight_workspace]*2,
        urgent_alert_method = 'border',
        borderwidth = 2,
        disable_drag = True
    ),

    widget.Sep(padding=space_width, linewidth=separator_line),

    widget.CurrentLayoutIcon(
        padding = 0,
        scale = 0.7
    ),

    widget.Sep(padding=space_width, linewidth=separator_line),

    widget.Prompt(),
    widget.Chord(
        chords_colors={
            'launch': ("#ff0000", "#ffffff"),
        },
        name_transform=lambda name: name.upper(),
    ),

    widget.Spacer(length = space_width),


    #widget.WindowName(
    #    foreground = focus_color,
    #    max_chars = 50,
    #),
    widget.TaskList(
        border = "#ffffff",
        borderwidth = 1,
        hightlight_method = "border",
        max_title_width = 200,
        icon_size = None,
    ),
]


# widget on the right
def init_right_widgets(pc_mode = "laptop"):
    widget_sysmonitor = [
        widget.Net(
            format = "netspeed: {down} ↓↑ {up}",
            interface = "wlp1s0",
            update_interval = 2,
            use_bits = False,
        ),

        widget.Spacer(length = space_width),
        widget.Image(
            margin_y = 5,
            filename = "~/.config/qtile/icons/cpu-svgrepo-com.svg"
        ),
        widget.CPUGraph(
            border_color = "#000000",
            graph_color = "#ffffff",
            type = 'box',
            frequency = 1
        ),

        widget.Spacer(length = space_width),
        widget.Image(
            margin_y = 5,
            filename = "~/.config/qtile/icons/temperature-svgrepo-com.svg"
        ),
        widget.ThermalSensor(
            fmt = "{}",
            update_interval = 5,
            #tag_sensor="edge"
        ),

        widget.Spacer(length = space_width),
        widget.Image(
            margin_y = 5,
            filename = "~/.config/qtile/icons/ram-svgrepo-com.svg"
        ),
        widget.Memory(
            format = "{MemUsed: .2f}{mm}/{MemTotal: .2f}{mm}",
            measure_mem = "G",
            update_interval = 2,
        ),
    ]

    widget_laptop = [
        widget.Spacer(length = space_width),
        widget.Image(
            margin_y = 5,
            filename = "~/.config/qtile/icons/brightness-svgrepo-com.svg"
        ),
        widget.Backlight(
            fmt = "{}",
            change_command = 'brightnessctl set {0}',
            brightness_file = '/sys/class/backlight/amdgpu_bl0/brightness',
            max_brightness_file = '/sys/class/backlight/amdgpu_bl0/max_brightness'
        ),

        widget.Spacer(length = space_width),
        widget.Image(
            margin_y = 5,
            filename = "~/.config/qtile/icons/battery-full-battery-svgrepo-com.svg"
        ),
        widget.Battery(
            format = '{percent:2.0%}',
            full_char = "bat: Full"
        ),
    ]

    widget_general = [
        widget.Spacer(length = space_width),
        widget.Image(
            margin_y = 5,
            filename = "~/.config/qtile/icons/volume-audio-svgrepo-com.svg"
        ),
        widget.Volume(
            fmt = "{}",
        ),

        widget.Spacer(length = space_width),
        widget.Image(
            margin_y = 5,
            filename = "~/.config/qtile/icons/calendar-svgrepo-com.svg"
        ),
        widget.Clock(
           format = '%a, %d-%b-%y %H:%M',
        ),
        widget.Systray()
    ]

    if pc_mode == "desktop":
        right_widgets = widget_sysmonitor + widget_general
    elif pc_mode == "laptop":
        right_widgets = widget_sysmonitor + widget_laptop + widget_general

    return right_widgets

right_widgets = init_right_widgets(pc_mode = pc_mode)


# bar configuration
bar_top = 0
bar_right = 0
bar_bottom = 0
bar_left = 0
general_bar_setting = {
	'size' : 26,
    'opacity': 1,
    'margin': [bar_top, bar_right, bar_bottom, bar_left]
}


screens =  [
    Screen(top=bar.Bar(widgets=left_widgets + right_widgets,
        **general_bar_setting)
        ),
    Screen(top=bar.Bar(widgets=left_widgets + right_widgets[:-1],
        **general_bar_setting)
    )
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
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
        border_focus = focus_color,
        border_width = border_w,
        float_rules = [
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry

    # specific application
    Match(wm_class="Gnome-calculator"),
    Match(wm_class="Galculator"),
    Match(wm_class="zoom"),
    Match(wm_class="File-roller"),
    Match(wm_class="xarchiver")
])

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True


# autostart application
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])



# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
