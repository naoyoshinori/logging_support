# logging_support

This [logging_support](https://github.com/naoyoshinori/logging_support) library controls the log output of the application and library. Log data is output to both terminal and file.

## 1. Install

```bash
pip install https://github.com/naoyoshinori/logging_support/archive/main.zi
```

## 2. Usage

### 2.1 Import package

```python
from logging import getLogger, WARNING, INFO, DEBUG
from logging_support import initialize_logger
```

### 2.2 Create a logger

```python
logger = getLogger(__name__)
```

### 2.3 Initialize logger

```python
initialize_logger(
    name="example",
    dir="logs",
    fmt="%(levelname)s:%(name)s:%(message)s",
    level="WARNING",
    handler_level=DEBUG,
)
```

### 2.4 List of options to initialize logger.

| Keyword | Description |
|---|---|
| name | Set a name for logging. |
| dir | Set a folder to save logging files. The default directory is 'logs'. |
| filename | Set the file name for logging. The default file name is '{dir}/{name}.log'. |
| fmt | This string sets the format for logging. |
| level | Set the level of logging. |
| handler_level | Set the level of the handler for logging. |

### 2.5 Logging

See the Python logging documentation for details.

```python
logger.debug("debug message.")
logger.info("info message.")
logger.warning("warning message.")
logger.error("error message.")
```

### 2.6 For third-party libraries

Third-party libraries can also configure log output.

```python
from logging import getLogger, WARNING, INFO, DEBUG
from logging_support import initialize_logger

import selenium
from selenium import webdriver

initialize_logger(name="selenium", level=WARNING)
 or
initialize_logger(name=selenium.__name__, level=WARNING)
 or
initialize_logger(name=webdriver.__name__, level=WARNING)
```

## 3. Example

Example of directory structure.

```bash
example
│  example.py
│  
└─mypackage
       __init__.py
```

Here is an example of a custom package.

```python:mypackage/__init__.py
from logging import getLogger

logger = getLogger(__name__)


def hello():
    logger.debug("hello, world!")
```

Here is an example of the main program.

```python:example.py
from logging import getLogger, WARNING, INFO, DEBUG
from logging_support import initialize_logger

import mypackage

logger = getLogger(__name__)

initialize_logger(name=__name__, level=DEBUG)
initialize_logger(name=mypackage.__name__, level=DEBUG)

logger.debug("message")

mypackage.hello()
```

The logging results are displayed in the terminal. 

```
DEBUG:__main__:message
DEBUG:mypackage:hello, world!
```

In addition, logging results are output as a file. The files 'logs/__main__.log' and 'logs/mypackage.log' are created.

```bash
example
│  example.py
│  
├─mypackage
│      __init__.py
│      
└─logs
       __main__.log
       mypackage.log
```
