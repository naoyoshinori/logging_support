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
    dir: str = "logs",
    filename: str = None,
    fmt: str = DEFAULT_FORMAT,
    datefmt: str = None,
    level: int | str = logging.WARNING,
    handler_level: int | str = logging.NOTSET,
    maxBytes: int = 500,
    backupCount: int = 2,
) -> None:
    """
    Initialize the Simple logger.

    Args:
        name: Set a name for logging.
        dir: Set a folder to save logging files.
            The default directory is 'logs'.
        filename: Set the file name for logging.
            The default file name is '{dir}/{name}.log'.
        fmt: This string sets the format for logging.
            The default format is "%(asctime)s %(levelname)s %(name)s - %(message)s"
        datefmt: Set the date format. The default is ISO-8601 Format.
        level: Set the level of logging.
        handler_level: Set the level of the handler for logging.
        maxBytes: File size for logging. The default is 500 bytes.
        backupCount: Backup counts for logging. The default is two files.
    """

    if filename is None:
        filename = f"{dir}/{name}.log"

    os.makedirs(dir, exist_ok=True)

    formatter = ISO8601_Formatter(fmt, datefmt=datefmt)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(handler_level)

    file_handler = logging.handlers.RotatingFileHandler(
        filename, maxBytes=maxBytes, backupCount=backupCount
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(handler_level)

    logger = logging.getLogger(name)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(level)
