from pathlib import Path


CORE_DIR = Path(__file__).parent
BASE_DIR = CORE_DIR.parent

GUI_DIR = CORE_DIR.joinpath("gui")
GUI_IMAGES = GUI_DIR.joinpath("images")
GUI_ICONS = GUI_DIR.joinpath("icons")

IMG_DIR = BASE_DIR.joinpath("images")

LOG_DIR = BASE_DIR.joinpath("log")
SETTINGS_DIR = CORE_DIR.joinpath("settings")

LOG_DIR.mkdir(exist_ok=True)
IMG_DIR.mkdir(exist_ok=True)
SETTINGS_DIR.mkdir(exist_ok=True)