"""Logger configuration module for file organization application."""

import logging
from pathlib import Path
from typing import Optional


def setup_logging(
    log_file: Optional[Path] = None,
    verbose: bool = False,
) -> logging.Logger:
    """Configure application-wide logging handlers and levels.

    :param log_file: Optional path to write log messages to disk.
    :param verbose: If True, set log level to DEBUG, otherwise INFO.
    :return: Root application logger.
    """
    logger = logging.getLogger("file_organizer")
    logger.handlers.clear()

    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)

    # Console Handler
    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Optional File Handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # Always log verbose details to file if requested
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
