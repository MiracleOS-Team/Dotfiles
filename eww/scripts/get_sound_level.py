#!/bin/python3.11
import subprocess
import os

dt = int(subprocess.check_output(["bash", "scripts/getvol"]).decode("utf-8"))

if dt >= 85:
    print("audio-volume-high-symbolic")
elif dt >= 25:
    print("audio-volume-medium-symbolic")
elif dt > 0:
    print("audio-volume-low-symbolic")
elif dt == 0:
    print("audio-volume-muted-symbolic")
else:
    print("audio-speakers-symbolic")