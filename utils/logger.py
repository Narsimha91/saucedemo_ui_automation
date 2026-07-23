"""Logging utility module."""

import logging
import os


def get_logger(name):
    """Create and return logger."""

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Create logs folder
    os.makedirs("logs", exist_ok=True)

    file_handler = logging.FileHandler(
        "logs/ui_automation.log"
    )

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger