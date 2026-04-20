import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(name: str = "fastapi_app", level: str = "INFO"):
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    # Format for logs
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level.upper())


    if logger.hasHandlers():
        logger.handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))


    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=1_000_000, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(log_format))


    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger