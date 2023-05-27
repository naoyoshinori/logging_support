# logging_support

[logging_support](https://github.com/naoyoshinori/logging_support) is a simple logging library for Python. This library outputs log data to both the console and a file. Logging is configured on a module-by-module basis, without using the `basicConfig` of the Python standard library [logging](https://docs.python.org/3/library/logging.html).

## 1. Install

```bash
pip install https://github.com/naoyoshinori/logging_support/archive/main.zip
```

## 2. Usage

### 2.1 Import packages

For logging in the main program.

```python
from logging import getLogger, WARNING, INFO, DEBUG
from logging_support import initialize_simple_logger
```

For logging with the module.

```python
from logging import getLogger
```

### 2.2 Create Logger

```python
logger = getLogger(__name__)
  or
logger = getLogger("example")
```

The module name can be set by using `__name__` in the logger name.

### 2.3 Initialize Simple Logger

Initialize the logger in the main program as follows. Set the module name to `name`. Set `dir` to the directory where log data is stored.


```python
initialize_simple_logger(
    name="example",
    dir="logs",
    fmt="%(levelname)s:%(name)s:%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level="WARNING",
    handler_level=DEBUG,
    maxBytes=500,
    backupCount=2,
)
```

### 2.4 List of options.

| Keyword | Description |
|---|---|
| name | Set a name for logging. |
| dir | Set a folder to save logging files. The default directory is 'logs'. |
| filename | Set the file name for logging. The default file name is '{dir}/{name}.log'. |
| fmt | This string sets the format for logging. The default format is "%(asctime)s %(levelname)s %(name)s - %(message)s" |
| datefmt | Set the date format. The default is ISO-8601 Format. |
| level | Set the level of logging. level must be an int or a str. |
| handler_level | Set the level of the handler for logging. level must be an int or a str. |
| maxBytes | File size for logging. The default is 500 bytes. |
| backupCount | Backup counts for logging. The default is two files. |

### 2.5 Logging

For more information on logging, see the documentation of the Python standard library [logging](https://docs.python.org/3/library/logging.html).

```python
logger.debug("debug message.")
logger.info("info message.")
logger.warning("warning message.")
logger.error("error message.")
```

### 2.6 For third-party libraries

Log output can also be configured in third-party libraries.

```python
from logging import getLogger, WARNING, INFO, DEBUG
from logging_support import initialize_simple_logger

import selenium

initialize_simple_logger(name="selenium", level=DEBUG)
  or
initialize_simple_logger(name=selenium.__name__, level=DEBUG)
```

## 3. Example

The directory structure of Example.

```bash
example
│  example.py
│  
└─mypackage
   __init__.py
```

Here is an example of mypackage, which uses `getLogger` from the Python standard logging library.

```python
# mypackage/__init__.py
from logging import getLogger

logger = getLogger(__name__)

def hello():
    logger.debug("hello, world!")
```

Here is an example of the main program. Here we initialize the logger for each module, using `basicConfig` from the Python standard library logging, there is a problem with all logs being output.

```python
# example.py
from logging import getLogger, WARNING, INFO, DEBUG
from logging_support import initialize_simple_logger

import mypackage

logger = getLogger("main")

initialize_simple_logger(name="main", level=DEBUG)
initialize_simple_logger(name=mypackage.__name__, level=DEBUG)

logger.debug("message")

mypackage.hello()
```

This library displays log data on the console.

```bash
2023-05-27T07:20:32.798+09:00 DEBUG main - message
2023-05-27T07:20:32.798+09:00 DEBUG mypackage - hello, world!
```

In addition, it outputs log data as files `logs/main.log` and `logs/mypackage.log` in the case of Example.

```bash
example
│  example.py
│  
├─mypackage
│  __init__.py
│      
└─logs
   main.log
   mypackage.log
```
