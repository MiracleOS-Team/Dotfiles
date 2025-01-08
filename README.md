# Miracle OS dotfiles (WIP)

This is a repo for MiracleOS's dotfiles. You can git clone them and symlink to your local config.

Things dynamic:

* app list
* sound icon
* battery icon
* ethernet icon
* time
* notifications

Everything else is just placeholders

## Needed software

* labwc
* eww
* swaybg
* mako
* swayidle
* firefox
* alacritty
* python3.11
* networkmanager
* pavucontrol
* MiracleOS's notification daemon (will crash if not installed)
* inotify-tools

## Recommended software

* wdisplays

## Needed modifications

modify XKB_DEFAULT_lAYOUT in labwc/environment to your keyboard layout

## Specifications
### Fully compatible

- https://specifications.freedesktop.org/notification-spec/latest/

### Partially compatible (or bad implementation)

- https://specifications.freedesktop.org/basedir-spec/latest/
- https://specifications.freedesktop.org/desktop-entry-spec/latest/
- https://specifications.freedesktop.org/icon-theme-spec/latest/


### Soon compatible

- https://specifications.freedesktop.org/autostart-spec/latest/
- https://specifications.freedesktop.org/menu-spec/latest/
