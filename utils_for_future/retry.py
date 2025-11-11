import time
import functools
import enum

class RetryStrategies(enum.StrEnum):
    EXPONENTIAL = "exponential"
    LINEAR = "linear"

def retry(
    retries: int = 3,
    delay: float = 1.0,
    strategy: RetryStrategies = RetryStrategies.EXPONENTIAL,
):
    """Retry decorator with configurable backoff strategy.

        This decorator automatically retries a function call that raises an exception.
        It supports both **linear** and **exponential** backoff strategies for controlling
        the delay between retry attempts.

        Example:
            ```python
            @retry(retries=5, delay=1.0, strategy=RetryStrategies.EXPONENTIAL)
            def flaky_function():
                if random.random() < 0.8:
                    raise ValueError("Temporary error")
                return "Success"

            result = flaky_function()
            ```

        Args:
            retries (int):
                Number of retry attempts before giving up.
            delay (float):
                Base delay in seconds between retries.
            strategy (RetryStrategies):
                Backoff strategy to use — either:
                  - `RetryStrategies.EXPONENTIAL`: delay doubles each attempt (1s, 2s, 4s…)
                  - `RetryStrategies.LINEAR`: delay increases linearly (1s, 2s, 3s…)

        Returns:
            Callable:
                A decorated version of the function that will retry automatically
                upon exceptions.

        Raises:
            Exception:
                The last caught exception if all retries fail for simplicity.
        """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt >= retries:
                        raise
                    sleep_for = delay * attempt
                    if strategy == RetryStrategies.EXPONENTIAL:
                        sleep_for = delay * (2 ** (attempt - 1))
                    # put loguru here
                    print(f"[retry] attempt {attempt}/{retries} failed: {e!r}. retrying in {sleep_for:.2f}s")
                    time.sleep(sleep_for)
        return wrapper
    return decorator