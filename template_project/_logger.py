import logging
import sys

import orjson
import structlog

shared_processors = [
    # Processors that have nothing to do with output,
    # e.g., add timestamps or log level names.
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso", utc=True),
    structlog.processors.CallsiteParameterAdder(
        {
            structlog.processors.CallsiteParameter.FILENAME,
            structlog.processors.CallsiteParameter.FUNC_NAME,
            structlog.processors.CallsiteParameter.LINENO,
        }
    ),
    structlog.processors.format_exc_info,
]
if sys.stderr.isatty():
    processors = shared_processors + [
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.dev.ConsoleRenderer(),
    ]
    factory = structlog.PrintLoggerFactory()

else:
    processors = shared_processors + [
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(serializer=orjson.dumps),
    ]
    factory = structlog.BytesLoggerFactory()


structlog.configure(
    cache_logger_on_first_use=True,
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=processors,
    logger_factory=factory,
)
