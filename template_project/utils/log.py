"""
This is aimed to replace print. To use the implemented config do:

from loans.utils.log import get_logger

logger = get_logger()
"""


import enum
import functools
import sys
import time

from loguru import logger


class LogLevels(str, enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"


LOG_FILE = "loans.log"
LOG_LEVEL = LogLevels.DEBUG


def configured_logger_factory():
    logger.remove()
    logger.add(LOG_FILE, level=LOG_LEVEL)
    if LOG_LEVEL == LogLevels.INFO:
        logger.add(
            sys.stderr,
            level=LOG_LEVEL,
            format="{time: YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        )
    elif LOG_LEVEL == LogLevels.DEBUG:
        logger.add(sys.stderr, level=LOG_LEVEL)
    else:
        raise Exception
    return logger


def get_logger():
    return configured_logger_factory()


def logger_wraps(
    *,
    entry: bool = True,
    exit: bool = True,
    level: str = LogLevels.DEBUG,
):
    """
    What does this answer?
     - When did the function execution started and with which params?
     - How much time does the function took to run?
     - When did the function execution finished and with with result?

    @logger_wraps()
    def some_function():
        return ...
    """

    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(
                    level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs
                )
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            logger_.log(level, "Function '{}' executed in {:f} s", name, end - start)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper
