# Standard Library
import inspect
import time
from contextlib import asynccontextmanager, contextmanager
from functools import wraps
from typing import Any, AsyncGenerator, Callable, Generator

# Project
from app.config import LOGGER


def wrap_timer(name: str) -> Callable:
    def wrapper(fun: Callable) -> Callable:
        if inspect.iscoroutinefunction(fun):

            @wraps(fun)
            async def wrap(*args: Any, **kw: Any) -> Any:
                ts = time.perf_counter()
                result = await fun(*args, **kw)
                te = time.perf_counter()
                LOGGER.info(f"{name}: total execution time: {(te - ts):.3f} seconds")
                return result

            return wrap

        else:

            @wraps(fun)
            def wrap(*args: Any, **kw: Any) -> Any:
                ts = time.perf_counter()
                result = fun(*args, **kw)
                te = time.perf_counter()
                LOGGER.info(f"{name}: total execution time: {(te - ts):.3f} seconds")
                return result

            return wrap

    return wrapper


@asynccontextmanager
async def aio_ctx_timer(name: str) -> AsyncGenerator[None, None]:
    ts = time.perf_counter()
    yield
    te = time.perf_counter()
    LOGGER.info(f"{name}: total execution time: {(te - ts):.3f} seconds")


@contextmanager
def ctx_timer(name: str) -> Generator[None, None, None]:
    ts = time.perf_counter()
    yield
    te = time.perf_counter()
    LOGGER.info(f"{name}: total execution time: {(te - ts):.3f} seconds")
