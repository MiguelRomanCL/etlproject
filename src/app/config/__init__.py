# Local
from .config import (
    POSTGRES_DATABASE,
    POSTGRES_PASSWORD,
    POSTGRES_SERVER,
    POSTGRES_USER,
    PROJECT_NAME,
    VERSION,
)
from .logger import LOGGER_NAME, create_logger


LOGGER = create_logger(logger_name=LOGGER_NAME, handlers=["console", "file"])

__all__ = [
    "LOGGER",
    "LOGGER_NAME",
    "create_logger",
    "POSTGRES_DATABASE",
    "POSTGRES_PASSWORD",
    "POSTGRES_SERVER",
    "POSTGRES_USER",
    "PROJECT_NAME",
    "VERSION",
]
