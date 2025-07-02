import time
from loguru import logger


class TimingContextManager:
    def __init__(
        self,
        *,
        name: str,
        level: str = "DEBUG",
    ) -> None:
        self.name: str = name
        self.level: str = level
        self.t_start: float = 0
        self.log = logger.opt(lazy=True).bind(session_name=self.name)

    async def __aenter__(self):
        self.t_start = time.perf_counter()
        self.log.log(self.level, f"Session '{self.name}' started.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        duration = time.perf_counter() - self.t_start
        if any((exc_type, exc_val, exc_tb)):
            self.log.exception(f"Exception during session '{self.name}'")
        self.log.bind(duration=duration).log(
            self.level,
            f"Session '{self.name}' finished successfully.",
        )
