import sys
import platform

import PyInstaller.__main__
from PyInstaller.building.api import EXE


EXE()

OS = platform.system()


if OS == "Windows":
    PyInstaller.__main__.run([
        "image_generator.py",
        "--clean",
        "--onefile",
        "--runtime-tmpdir=.",
        "--icon=icon.ico",
        "--name=ImageGenerator.exe"
    ])
else:
    sys.exit(1)