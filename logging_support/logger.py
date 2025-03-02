import logging
import logging.handlers
import os

from datetime import datetime, timezone

DEFAULT_FORMAT = "%(asctime)s %(levelname)s %(name)s - %(message)s"


class ISO8601_Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        if datefmt:
            s = super().formatTime(record, datefmt)
        else:
            # Adopt the ISO-8601 Format for Timestamps
            s = (
                datetime.fromtimestamp(record.created, timezone.utc)
                .astimezone()
                .isoformat(sep="T", timespec="milliseconds")
            )
        return s


def initialize_simple_logger(
    name: str,
    log_dir: str = "logs",
    filename: str = None,
    fmt: str = DEFAULT_FORMAT,
    datefmt: str = None,
    level: int | str = logging.WARNING,
    stream_handler_level: int | str = None,
    file_handler_level: int | str = None,
    maxBytes: int = 10 * 1024 * 1024, # 10MB
    backupCount: int = 2,
) -> logging.Logger:
    """
    Initialize the Simple logger.

    Args:
        name: The name of the logger.
        log_dir: Directory for log files. Default: "logs".
        filename: Log file name. Default: "{log_dir}/{name}.log".
        fmt: Log message format. Default: "%(asctime)s %(levelname)s %(name)s - %(message)s".
        datefmt: Date format. Default: ISO-8601 (e.g., "2023-05-27T07:20:32.798+09:00").
        level: Logger level (int or str). Default: logging.WARNING.
        stream_handler_level: Stream handler level. Default: if `None`, the parameter `level` is used.
        file_handler_level: File handler level. Default: if `None`, the parameter `level` is used.
        maxBytes: Max file size before rotation. Default: 10MB.
        backupCount: Number of backup log files. Default: 2.
    Returns:
        The configured logger instance.
    """

    if filename is None:
        filename = os.path.join(log_dir, f"{name}.log")

    os.makedirs(log_dir, exist_ok=True)

    if stream_handler_level is None:
        stream_handler_level = level
    
    if file_handler_level is None:
        file_handler_level = level

    formatter = ISO8601_Formatter(fmt, datefmt=datefmt)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(stream_handler_level)

    file_handler = logging.handlers.RotatingFileHandler(
        filename, maxBytes=maxBytes, backupCount=backupCount
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_handler_level)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if logger.handlers:
        logger.warning("Overwriting existing handlers for '%s' logger", name)
        logger.handlers.clear()
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
