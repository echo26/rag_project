import logging
import logging.config
from pathlib import Path

_LOG_DIR = Path("var/log")

_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)-8s %(name)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
        "access": {
            "format": "%(asctime)s ACCESS %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },
    "handlers": {
        "debug": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "default",
            "filename": str(_LOG_DIR / "debug.log"),
            "when": "midnight",
            "backupCount": 7,
            "encoding": "utf-8",
            "level": "DEBUG",
        },
        "error": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "default",
            "filename": str(_LOG_DIR / "error.log"),
            "when": "midnight",
            "backupCount": 7,
            "encoding": "utf-8",
            "level": "ERROR",
        },
        "access": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "access",
            "filename": str(_LOG_DIR / "access.log"),
            "when": "midnight",
            "backupCount": 7,
            "encoding": "utf-8",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["debug", "error"],
    },
    "loggers": {
        "uvicorn.access": {
            "handlers": ["access"],
            "propagate": False,
        },
        "uvicorn.error": {"propagate": True},
        "gunicorn.access": {
            "handlers": ["access"],
            "propagate": False,
        },
        "gunicorn.error": {"propagate": True},
    },
}


def setup_logging() -> None:
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(_CONFIG)
