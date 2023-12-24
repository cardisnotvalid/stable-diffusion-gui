import sys
from loguru import logger


LOG_FORMAT = "<green>{time:HH:mm:ss}</green> - <level>{level: <8}</level> - <white>{message}</white>"


def setup_logger(debug: bool = False) -> None:
    logger.remove()
    logger.add(sys.stdout, level="DEBUG" if debug else "INFO", format=LOG_FORMAT)


setup_logger(True)