#!/bin/python3.11
import os
import configparser
import json

def find_icon(icon_name, icon_size=None, icon_dirs=None, icon_extensions=None):
    """Search for an icon in standard directories with optional size preference."""
    if icon_dirs is None:
        pre_icon_dirs = [
            os.path.join(os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share")), "icons"),
            "/usr/share/icons",
            "/usr/local/share/icons",
            os.path.join(os.environ.get("HOME", ""), ".icons"),
        ]
        icon_dirs = ["/usr/share/icons/MiracleOSIcons"]

        for id in pre_icon_dirs:
            try:
                icon_dirs += [os.path.join(id, k) for k in os.listdir(id)]
            except:
                pass
    if icon_extensions is None:
        icon_extensions = [".png", ".svg", ".xpm"]

    # Generate a list of potential sizes to try (progressively larger and smaller)
    size_range = [icon_size] if icon_size else []
    if icon_size:
        size_range += [size for size in range(icon_size, 257, 1)]  # Larger sizes
        size_range += [size for size in range(icon_size, 0, 1)]   # Smaller sizes

    for size in size_range:
        for directory in icon_dirs:
            for walkable in [os.walk(directory+f"/{str(size)}x{str(size)}"), os.walk(directory+f"/{str(size)}x{str(size)}@2x")]:
                for root, dirs, files in walkable:
                    if f"{str(size)}x{str(size)}" in root:
                        for ext in icon_extensions:
                            if f"{icon_name}{ext}" in files:
                                return os.path.join(root, f"{icon_name}{ext}")

    return None

def parse_desktop_file(filepath):
    """Parse a .desktop file to extract the Icon field."""
    config = configparser.ConfigParser(interpolation=None)
    config.read(filepath)
    if "Desktop Entry" in config and "Icon" in config["Desktop Entry"]:
        return config["Desktop Entry"]["Icon"]
    return None

def save_to_app_cache(app_name, fallback_icon, icon_size, final_path):
    try:
        dt = json.load(open(os.path.join(os.getenv("HOME"), ".config/miracleos/app-icons.json"), "r"))

        dt[f"{app_name}-{icon_size}-{fallback_icon}"] = final_path

        json.dump(dt, open(os.path.join(os.getenv("HOME"), ".config/miracleos/app-icons.json"), "w"), indent=4)
    except:
        pass

def get_cached_app(app_name, fallback_icon, icon_size):
    try:
        dt = json.load(open(os.path.join(os.getenv("HOME"), ".config/miracleos/app-icons.json"), "r"))
        if f"{app_name}-{icon_size}-{fallback_icon}" in dt:
            return dt[f"{app_name}-{icon_size}-{fallback_icon}"]
        else:
            return None
    except:
        return None

def get_app_alias(app_name):
    try:
        dt = json.load(open(os.path.join(os.getenv("HOME"), ".config/miracleos/app-icons-alias.json"), "r"))
        if app_name in dt:
            return dt[app_name]
        else:
            return app_name
    except:
        return app_name

def get_application_logo(app_name: str, fallback_icon: str = "application-x-executable", icon_size: int = 256) -> str:
    """
    Get the application logo from the system icon theme or desktop files.

    :param app_name: The name of the application (as used in .desktop files or icon names).
    :param fallback_icon: Icon to return if the application icon is not found.
    :param icon_size: Preferred size of the icon (e.g., 48 for 48x48 icons).
    :return: Path to the application icon or the fallback icon.
    """

    app_name = get_app_alias(app_name)

    cached_app_icon = get_cached_app(app_name, fallback_icon, icon_size)
    if cached_app_icon != None:
        return cached_app_icon


    # Try to locate the icon directly in the current theme first
    icon_path = find_icon(app_name, icon_size=icon_size)
    if icon_path:
        save_to_app_cache(app_name, fallback_icon, icon_size, icon_path)
        return icon_path

    # Search in .desktop files if the icon is not found in the theme
    desktop_dirs = [
        os.path.join(os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share")), "applications"),
        "/usr/share/applications",
        "/usr/local/share/applications",
    ]

    for directory in desktop_dirs:
        desktop_file_path = os.path.join(directory, f"{app_name}.desktop")
        if os.path.exists(desktop_file_path):
            icon_name = parse_desktop_file(desktop_file_path)
            if icon_name:
                icon_path = find_icon(icon_name, icon_size=icon_size)
                if icon_path:
                    save_to_app_cache(app_name, fallback_icon, icon_size, icon_path)
                    return icon_path

    # Fallback to a default icon
    if not app_name.islower():
        icon_path = get_application_logo(app_name=app_name.lower(), fallback_icon=fallback_icon, icon_size=icon_size)
        return icon_path
    fallback_path = find_icon(fallback_icon, icon_size=icon_size)
    save_to_app_cache(app_name, fallback_icon, icon_size, fallback_path)
    return fallback_path
