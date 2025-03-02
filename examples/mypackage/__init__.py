# mypackage/__init__.py
from logging import getLogger

logger = getLogger(__name__)


def hello():
    logger.debug("Hello, world!")
