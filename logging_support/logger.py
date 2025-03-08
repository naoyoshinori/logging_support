import logging
import logging.handlers
import os

from datetime import datetime, timezone
from logging import getLogger
from zoneinfo import ZoneInfo

DEFAULT_FORMAT = "%(asctime)s %(levelname)s %(name)s - %(message)s"
DEFAULT_MAX_BYTES = 10 * 1024 * 1024  # 10MB
DEFAULT_BACKUP_COUNT = 2


class ISO8601_Formatter(logging.Formatter):
    def __init__(
        self,
        fmt=None,
        datefmt=None,
        tz=None,
        style="%",
        validate=True,
        *,
        defaults=None,
    ):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)
        # Set timezone
        if tz:
            self._tz = ZoneInfo(tz)
        else:
            self._tz = None

    def formatTime(self, record, datefmt=None):
        if datefmt:
            # Use the provided datefmt
            s = super().formatTime(record, datefmt)
        else:
            # Use ISO-8601 format (e.g., "2023-05-27T07:20:32.798+09:00")
            # if _tz attribute is set to None, the timezone is local time.
            s = (
                datetime.fromtimestamp(record.created, timezone.utc)
                .astimezone(tz=self._tz)
                .isoformat(timespec="milliseconds")
            )
        return s


def initialize_simple_logger(
    name: str,
    log_dir: str = "logs",
    filename: str = None,
    fmt: str = DEFAULT_FORMAT,
    datefmt: str = None,
    tz: str = None,
    formatter: logging.Formatter = None,
    level: int | str = logging.WARNING,
    stream_handler_level: int | str = None,
    file_handler_level: int | str = None,
    maxBytes: int = DEFAULT_MAX_BYTES,
    backupCount: int = DEFAULT_BACKUP_COUNT,
) -> logging.Logger:
    """
    Initialize the Simple logger.

    Args:
        name: The name of the logger.
        log_dir: Directory for log files. Default: "logs".
        filename: Log file name. Default: "{log_dir}/{name}.log".
        fmt: Log message format. Default: "%(asctime)s %(levelname)s %(name)s - %(message)s".
        datefmt: Date format. Default: ISO-8601 (e.g., "2023-05-27T07:20:32.798+09:00").
        tz: Timezone for log timestamps (e.g., "UTC", "Asia/Tokyo"). Default: None (local time).
        formatter: Custom formatter. Default: None (uses ISO8601_Formatter).
        level: Logger level (int or str). Default: logging.WARNING.
        stream_handler_level: Stream handler level. Default: if `None`, the parameter `level` is used.
        file_handler_level: File handler level. Default: if `None`, the parameter `level` is used.
        maxBytes: Max file size before rotation. Default: 10MB.
        backupCount: Number of backup log files. Default: 2.
    Returns:
        logging.Logger: The configured logger instance.
    Raises:
        ValueError: If any of the parameters are invalid.
        TypeError: If any of the parameters are of the wrong type.
    """

    # Validate name
    if name is None:
        raise ValueError("Logger name cannot be None")
    elif not isinstance(name, str):
        raise TypeError("Logger name must be a string")

    # Validate log_dir
    if log_dir is None:
        raise ValueError("Log directory cannot be None")
    elif not isinstance(log_dir, str):
        raise TypeError("Log directory must be a string")

    # Validate maxBytes
    if (not isinstance(maxBytes, int)) or (maxBytes < 0):
        raise ValueError("maxBytes must be a positive integer")

    # Validate backupCount
    if (not isinstance(backupCount, int)) or (backupCount < 0):
        raise ValueError("backupCount must be a positive integer")

    # stream_handler_level and file_handler_level default to parameter 'level'
    if stream_handler_level is None:
        stream_handler_level = level

    if file_handler_level is None:
        file_handler_level = level

    # mylogger is used to log messages during initialization
    mylogger = getLogger(__name__)
    if mylogger.handlers == []:
        myhandler = logging.StreamHandler()
        myhandler.setFormatter(ISO8601_Formatter(DEFAULT_FORMAT, tz="UTC"))
        myhandler.setLevel(logging.NOTSET)
        mylogger.addHandler(myhandler)

    # mylogger uses stream_handler_level
    mylogger.setLevel(stream_handler_level)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create formatter
    if formatter is None:
        formatter = ISO8601_Formatter(fmt, datefmt=datefmt, tz=tz)
    else:
        if fmt:
            mylogger.warning("Ignoring 'fmt' parameter when 'formatter' is provided")
        if datefmt:
            mylogger.warning(
                "Ignoring 'datefmt' parameter when 'formatter' is provided"
            )

    # Create log directory if it does not exist
    if not os.path.exists(log_dir):
        mylogger.info("Creating log directory: %s", log_dir)
        os.makedirs(log_dir, exist_ok=True)

    # Create log file path
    if filename is None:
        # Default log file path: {log_dir}/{name}.log
        logfile_path = os.path.join(log_dir, f"{name}.log")
    else:
        logfile_path = os.path.join(log_dir, filename)

    # if logger already has handlers, clear them
    if logger.handlers:
        mylogger.warning(
            "Logger already has handlers. Clearing existing handlers for '%s'", name
        )
        logger.handlers.clear()

    # Create stream and file handlers
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(stream_handler_level)

    file_handler = logging.handlers.RotatingFileHandler(
        logfile_path, maxBytes=maxBytes, backupCount=backupCount
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_handler_level)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
