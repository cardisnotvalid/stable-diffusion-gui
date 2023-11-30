import sys
from datetime import datetime

from loguru import logger

from core.paths import LOG_DIR


LOG_FORMAT = "<green>{time:HH:mm:ss}</green> - <level>{level: <8}</level> - <white>{message}</white>"
LOG_FILEPATH = LOG_DIR.joinpath(f"{datetime.now().strftime('%d-%m-%Y')}.log")


def setup_logger(debug: bool = False) -> None:
    logger.remove()
    logger.add(LOG_FILEPATH, level="DEBUG", format=LOG_FORMAT, rotation="1 day")
    logger.add(sys.stdout, level="DEBUG" if debug else "INFO", format=LOG_FORMAT)


setup_logger()