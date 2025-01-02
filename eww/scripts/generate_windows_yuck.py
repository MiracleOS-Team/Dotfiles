#!/bin/python3.11
import os
import subprocess
import get_app_icon

def get_win_list():
    dt = subprocess.check_output(["wlrctl", "toplevel", "list"]).decode("UTF-8")

    final = {}

    for a in dt.split("\n"):
        try:
            final[a.split(": ")[0]] = a.split(": ")[1]
        except:
            pass

    return final

def generate_buttons():
    dt1: dict[str, str] = get_win_list()

    returned = "(box "

    for app in dt1:
        returned += f"(button :class 'app' :onclick 'wlrctl toplevel activate title:\"{dt1[app]}\" app_id:\"{app}\"' (image :path '{get_app_icon.get_application_logo(app, icon_size=16)}'))\n"
    
    returned += ")"

    return returned

returned = '''
(box (button :class 'app' (image  :icon "firefox"))
 (button :class 'app' 'Bereuh'))
'''

print(generate_buttons())