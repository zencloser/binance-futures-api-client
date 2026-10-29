"""Configure rotating file logging and concise console warnings."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

DEFAULT_LOG_FILE = Path("logs") / "trading_bot.log"


def setup_logging(log_file=DEFAULT_LOG_FILE, level=logging.INFO) -> logging.Logger:
    """Configure the shared logger without adding duplicate handlers."""
    logger = logging.getLogger("trading_bot")
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_path, maxBytes=2_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.WARNING)
    logger.addHandler(console_handler)
    return logger
