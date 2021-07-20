# qtile-config
My own Qtile window manager config.

Requires psutil. Install it with:

pip install psutil

To enable the config, copy the files to ~/.config/qtile. Obviously, do this after you have installed Qtile.

WARNING! 
To get screenshot to work, edit the config and change wojnstup to your username at the bottom of the keybinds, where it says:
Key([mod, "shift"], "s", lazy.spawn("python3 /home/wojnstup/.config/qtile/screenshot.py"))
