import sys
from pathlib import Path


if getattr(sys, "frozen", False):
    CORE_DIR = Path(sys._MEIPASS).joinpath("core")
else:
    CORE_DIR = Path(__file__).parent

BASE_DIR = CORE_DIR.parent.parent

GUI_DIR = CORE_DIR.joinpath("gui")
GUI_IMAGES = GUI_DIR.joinpath("imgs")
GUI_ICONS = GUI_DIR.joinpath("icons")
GUI_CSS = GUI_DIR.joinpath("css")

IMG_DIR = BASE_DIR.joinpath("images")

SETTINGS_DIR = CORE_DIR.joinpath("settings")