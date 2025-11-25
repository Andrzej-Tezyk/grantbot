"""Custom logger."""

import logging

from app.utils.formatting import Formatter


def get_custom_logger(
    name: str,
    server_tag: str = "GENERIC",
) -> logging.Logger:
    """Create custom logger."""
    logger = logging.getLogger(name)
    
    logger.handlers.clear()
    logger.filters.clear()
    
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(Formatter())

    logger.addHandler(console_handler)

    class ServerContextFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            record.server = server_tag
            return True

    logger.addFilter(ServerContextFilter())

    return logger
