# logging_support

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

[logging_support](https://github.com/naoyoshinori/logging_support) is a simple Python library for logging. It outputs logs to both the console and a file without relying on the standard Python [logging.basicConfig](https://docs.python.org/3/library/logging.html). Logging can be configured between different modules.

## 1. Requirements

- Python 3.10 or higher (for full type hint support)
- tzdata (required on Windows for timezone support)

## 2. Installation

Install directly from GitHub:

```bash
pip install https://github.com/naoyoshinori/logging_support/archive/main.zip
```

## 3. Usage

### 3.1 Import Packages

For the main program:

```python
from logging import getLogger, WARNING, INFO, DEBUG
from logging_support import initialize_simple_logger
```

For modules:

```python
from logging import getLogger
```

### 3.2 Create Logger

Return a logger with the specified name. You can use the module name by using `__name__` in the logger name.

```python
logger = getLogger(__name__)
  or
logger = getLogger("example")
```

### 3.3 Initialize Simple Logger

Initialize the logger with custom settings. This function returns a configured logger.

```python
logger = initialize_simple_logger(
    name="example",
    log_dir="logs",
    fmt="%(asctime)s %(levelname)s %(name)s - %(message)s", # Custom format
    datefmt="%Y-%m-%dT%H:%M:%S", # Custom date format
    tz="Asia/Tokyo"
    level="DEBUG",
    file_handler_level=WARNING, # File logs warnings and above
    maxBytes=1024 * 1024, # 1MB (default is 10MB)
    backupCount=5, # 5 log files (default is 2)
)
```

#### Options

| Parameter | Description |
|---|---|
| name | The name of the logger. |
| log_dir | Directory for log files. Default: `"logs"`. |
| filename | Log file name. Default: `"{log_dir}/{name}.log"`. |
| fmt | Log message format. Default: `"%(asctime)s %(levelname)s %(name)s - %(message)s"`. |
| datefmt | Date format. Default: ISO-8601 (e.g., `"2023-05-27T07:20:32.798+09:00"`). |
| tz | Timezone for log timestamps (e.g., "UTC", "Asia/Tokyo"). Default: None (local time). |
| formatter | Custom formatter. Default: None (uses ISO8601_Formatter). |
| level | Logger level (int or str). Default: `logging.WARNING`. |
| stream_handler_level | Stream handler level. Default: if `None`, the parameter `level` is used. |
| file_handler_level | File handler level. Default: if `None`, the parameter `level` is used. |
| maxBytes | Max file size before rotation. Default: `10MB`. |
| backupCount | Number of backup log files. Default: `2`. |

> [!NOTE]
> On Windows, run `pip install tzdata` to use the `tz` parameter with specific timezones.

### 3.4 Logging Messages

See [Python's logging docs](https://docs.python.org/3/library/logging.html) for details. Use standard logging methods:

```python
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## 4. Example

### 4.1 Directory Structure

```bash
example/
│  example_usage.py
│  
└─mypackage/
   __init__.py
```

### 4.2 Module Example

```python
# mypackage/__init__.py
from logging import getLogger

logger = getLogger(__name__)

def hello():
    logger.debug("Hello, world!")
```

### 4.3 Main Program

```python
# example_usage.py
from logging import getLogger, WARNING, INFO, DEBUG
from logging_support import initialize_simple_logger

import mypackage

# Main logger with different levels for stream and file
logger = initialize_simple_logger(
    name="main",
    level=DEBUG,
    stream_handler_level=INFO,  # Console logs info and above
    file_handler_level=WARNING  # File logs warnings and above
)

# Module-specific logger
initialize_simple_logger(name=mypackage.__name__, level=DEBUG)

logger.debug("This is a debug message")  # Not displayed
logger.info("This is an info message")   # Only in file (if level allows)
logger.warning("This is a warning")      # Console and file
mypackage.hello()                        # Depends on mypackage logger
```

### 4.4 Output

#### Console:

```bash
2025-03-02T18:01:28.413+09:00 INFO main - This is an info message
2025-03-02T18:01:28.414+09:00 WARNING main - This is a warning
2025-03-02T18:01:28.414+09:00 DEBUG mypackage - Hello, world!
```

#### File `logs/main.log`:

```bash
2025-03-02T18:01:28.414+09:00 WARNING main - This is a warning
```

Files are stored in `logs/` with rotation (e.g. `main.log`, `main.log.1` etc.).

## 5. Features

- Logging can be configured for different modules.
- Supports standard output and file output.
- Supports log file rotation.
- Uses ISO-8601 as default date format.

## 6. Development

### 6.1 Virtual Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 6.2 Dependencies Installation

```bash
pip install -r requirements-dev.txt
```

### 6.3 Test Execution

```bash
pytest
```

### 6.4 Package Build

```bash
python -m build
```

## 7. Author
Developed by Naoyuki Yoshinori
