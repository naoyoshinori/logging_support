# example_usage.py
from logging import DEBUG, INFO, WARNING
from logging_support import initialize_simple_logger

import mypackage


def main():
    # Main logger with different levels for stream and file
    logger = initialize_simple_logger(
        name="main",
        level=DEBUG,
        stream_handler_level=INFO,  # Console logs info and above
        file_handler_level=WARNING,  # File logs warnings and above
    )

    # Module-specific logger
    initialize_simple_logger(name=mypackage.__name__, level=DEBUG)

    logger.debug("This is a debug message")  # Not displayed
    logger.info("This is an info message")  # Only in file (if level allows)
    logger.warning("This is a warning")  # Console and file
    mypackage.hello()  # Depends on mypackage logger


if __name__ == "__main__":
    main()
