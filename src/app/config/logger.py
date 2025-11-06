# Standard Library
import logging
import os
from logging.config import dictConfig


LOG_FOLDER = "./logs"

if not os.path.isdir(LOG_FOLDER):
    os.mkdir(LOG_FOLDER)

LOGGER_NAME = "msw-conversion-m"


def get_format(logger_name: str) -> str:
    return (
        '{"time": "%(asctime)s", "level": "%(levelname)s", '
        + '"thread": "%(threadName)s", "component": "%(module)s",'
        + f'"service": "{logger_name}", "payload": %(message)s}}'
    )


def get_config(logger_name: str, handlers: list[str] = ["file"]) -> dict:
    log_format = get_format(logger_name=logger_name)
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "class": "logging.Formatter",
                "format": log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": logging.INFO,
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "level": logging.DEBUG,
                "filename": f"{LOG_FOLDER}/{logger_name}.log",
                "mode": "a",
                "encoding": "utf-8",
                "maxBytes": 10_000_000,
                "backupCount": 4,
            },
        },
        "loggers": {
            logger_name: {
                "handlers": handlers,
                "level": logging.DEBUG,
                "propagate": False,
            },
        },
    }


def create_logger(logger_name: str, handlers: list[str] = ["file"]) -> logging.Logger:
    config = get_config(logger_name=logger_name, handlers=handlers)
    dictConfig(config)
    return logging.getLogger(logger_name)
