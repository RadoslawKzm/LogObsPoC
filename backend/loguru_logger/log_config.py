import json
import sys
import traceback

from asgi_correlation_id import correlation_id
from loguru import logger

from backend.loguru_logger import loguru_envs


# -- Filters & formats --
def safe_log(obj: str | dict) -> str:
    """Parsing dictionaries to avoid loguru key errors.
    When putting dict as lambda in lazy log,
    Loguru tends to unpack it and get provided dictionary as keys.
    This leads to keyerror in loguru.
    Adding parenthesis fixes problem.
    """
    if type(obj) != dict and type(obj) != str:
        try:
            obj = str(obj)
        except Exception:
            logger.critical(
                f"LOGURU EXCEPTION: safe_log parsing!!! {traceback.format_exc()}"
            )
    if type(obj) == dict:
        try:
            obj = json.dumps(obj, default=str)
        except Exception:
            logger.critical(
                f"LOGURU EXCEPTION: safe_log parsing!!! {traceback.format_exc()}"
            )
    return obj.replace("{", "{{").replace("}", "}}")


def correlation_id_filter(record: dict) -> bool:
    corr_id = correlation_id.get() or "No correlation_id"
    record["extra"]["correlation_id"] = corr_id
    return True


# HUMAN_FORMAT: str = (
#     "<level>{level: <8}</level>"
#     " | <green>{extra[correlation_id]}</green>"
#     " | <black>{time:YYYY-MM-DD HH:mm:ss.SSS}</black>"
#     " | <cyan>{name}</cyan>:<black>{function}</black>:<cyan>{line}</cyan> - "
#     "<level>{message}</level>"
# )


def human_readable_format(record):
    level = record["level"].name.ljust(8)
    corr_id = record["extra"].get("correlation_id", "No correlation_id")
    time = record["time"].strftime("%Y-%m-%d %H:%M:%S.%f")[
        :-3
    ]  # milliseconds precision
    name = record["name"]
    function = record["function"]
    line = record["line"]
    message = record["message"]


    return (
        f"<level>{level}</level> | "
        f"<green>{corr_id}</green> | "
        f"<black>{time}</black> | "
        f"<cyan>{name}</cyan>:<black>{function}</black>:<cyan>{line}</cyan> - "
        f"<level>{message}</level>\n"
    )


# -- Setup functions per sink --
def setup_console_human_logger():
    logger.add(
        sys.stderr,
        level=loguru_envs.CONSOLE_HUMAN_LOGGER_LEVEL,
        format=human_readable_format,
        filter=correlation_id_filter,
        enqueue=True,
        backtrace=False,
        diagnose=True,
        serialize=False,
        # rotation and retention do not apply to streams
    )


def setup_file_human_logger():
    logger.add(
        "logs/human_readable.log",
        level=loguru_envs.FILE_HUMAN_LOGGER_LEVEL,
        format=human_readable_format,
        filter=correlation_id_filter,
        rotation="2 hours",
        retention="2 hours",
        enqueue=True,
        backtrace=False,
        diagnose=True,
        serialize=False,
    )


def setup_safe_json_logger():
    logger.add(
        "logs/safe.json",
        level=loguru_envs.SAFE_JSON_LOGGER_LEVEL,
        format="{message}",
        filter=correlation_id_filter,
        rotation="1 hour",
        retention="7 days",
        enqueue=True,
        backtrace=False,
        diagnose=False,
        serialize=True,
    )


def setup_unsafe_json_logger():
    logger.add(
        "backend/logs/unsafe.json",
        level=loguru_envs.UNSAFE_JSON_LOGGER_LEVEL,
        format="{message}",
        filter=correlation_id_filter,
        rotation="1 hour",
        retention="1 day",
        enqueue=True,
        backtrace=False,
        diagnose=True,
        serialize=True,
    )


# -- Custom Levels --
# def _expected(self, message, *args, **kwargs):
#     return self.log("EXPECTED", message, *args, **kwargs)


# -- Setup function --
def logger_setup():
    logger.remove()
    logger.level("START", no=21, color="<green>", icon="🚀")
    logger.level("EXPECTED", no=24, color="<yellow>", icon="🤝")
    # logger.expected = _expected.__get__(logger)

    setup_console_human_logger()
    setup_file_human_logger()
    setup_safe_json_logger()
    setup_unsafe_json_logger()


# -- Log level docs for reference (optional) --
# flake8: noqa: E501
"""
TRACE (5): used to record fine-grained information about the program's execution path for diagnostic and analytics purposes.
DEBUG (10): used by developers to record messages for debugging purposes.
INFO (20): used to record informational messages that describe the normal operation of the program.
START (21): *CUSTOM* used only in middleware as indication of trace start.
EXPECTED (24): *CUSTOM* used for any hand risen HTTPException. App works ok, it is just not a SUCCESS.
SUCCESS (25): similar to INFO but used to indicate the success of an operation.
WARNING (30): used to indicate an unusual event that may require further investigation.
ERROR (40): used to record error conditions that affected a specific operation.
CRITICAL (50): used to record error conditions that prevent a core function from working.

+----------------------+------------------------+------------------------+
| Level name           | Severity value         | Logger method          |
+======================+========================+========================+
| ``TRACE``            | 5                      | logger.trace()         |
| ``DEBUG``            | 10                     | logger.debug()         |
| ``INFO``             | 20                     | logger.info()          |
| ``SUCCESS``          | 25                     | logger.success()       |
| ``WARNING``          | 30                     | logger.warning()       |
| ``ERROR``            | 40                     | logger.error()         |
| ``CRITICAL``         | 50                     | logger.critical()      |
+----------------------+------------------------+------------------------+
"""
# flake8: noqa: enable
