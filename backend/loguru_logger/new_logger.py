from typing import TYPE_CHECKING, Protocol, Any

from asgi_correlation_id import correlation_id
from loguru import logger as base_logger

if TYPE_CHECKING:
    from loguru._logger import Logger


class LoggerProtocol(Protocol):
    def trace(self, msg: Any, *args: Any, **kwargs: Any) -> None: ...
    def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None: ...
    def info(self, msg: Any, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, msg: Any, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: Any, *args: Any, **kwargs: Any) -> None: ...
    def critical(self, msg: Any, *args: Any, **kwargs: Any) -> None: ...


class AppLogger(LoggerProtocol):
    def __init__(self):
        self._loggers: dict[str, "Logger"] = {}

    def get(self) -> "Logger":
        cid = correlation_id.get()
        if cid not in self._loggers:
            self._loggers[cid] = base_logger.bind(correlation_id=cid)
        return self._loggers[cid]

    def __getattr__(self, name):
        # This magic method is called only if the attribute isn't found normally
        # Forward all unknown attribute accesses to the loguru logger
        return getattr(self.get(), name)


# Export a singleton instance
logger = AppLogger()
