import logging
import os


def initialize_logger(
    name: str,
    dir: str = "logs",
    filename: str = None,
    fmt: str = logging.BASIC_FORMAT,
    level: int | str = logging.WARNING,
    handler_level: int | str = logging.NOTSET,
) -> None:
    """
    Initialize the Logger.

    Args:
        name: Set a name for logging.
        dir: Set a folder to save logging files.
            The default directory is 'logs'.
        filename: Set the file name for logging.
            The default file name is '{dir}/{name}.log'.
        fmt: This string sets the format for logging.
        level: Set the level of logging.
        handler_level: Set the level of the handler for logging.
    """

    if filename is None:
        filename = f"{dir}/{name}.log"

    os.makedirs(dir, exist_ok=True)

    formatter = logging.Formatter(fmt)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(handler_level)

    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(handler_level)

    logger = logging.getLogger(name)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.setLevel(level)
