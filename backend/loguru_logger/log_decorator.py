import functools
import time

from loguru import logger


def log_it(log_level: str = "DEBUG", safe: bool = True):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            log = logger.opt(lazy=True).bind(function_name=func.__name__)
            if not safe:
                log = log.bind(function_args=args, function_kwargs=kwargs)
            log.log(log_level, f"Calling function '{func.__name__}'")

            try:
                t_start: float = time.perf_counter()
                result = await func(*args, **kwargs)
                t_end: float = time.perf_counter() - t_start
            except Exception:
                log = logger.opt(lazy=True).bind(function_name=func.__name__)
                if not safe:
                    log = log.bind(function_args=args, function_kwargs=kwargs)
                log.exception(
                    f"Exception occurred in function '{func.__name__}'"
                )
                raise

            end_log = logger.opt(lazy=True).bind(
                function_name=func.__name__,
                duration=t_end,
            )
            if not safe:
                end_log = end_log.bind(result=result)
            end_log.log(
                log_level, f"Function '{func.__name__}' finished successfully."
            )
            return result

        return wrapper

    return decorator
