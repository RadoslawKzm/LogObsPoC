from loguru import logger
import json
import traceback


def safe_log(obj: str | dict) -> str:
    """Parsing dictionaries to avoid loguru key errors.
    When putting dict as lambda in lazy log,
    Loguru tends to unpack it and get provided dictionary as keys.
    This leads to keyerror in loguru.
    Adding parenthesis fixes problem.
    """
    if not isinstance(obj, (str | dict)):
        try:
            obj = str(obj)
        except Exception:
            logger.critical(
                f"LOGURU EXCEPTION: safe_log parsing!!! "
                f"{traceback.format_exc()}"
            )
            raise
    if isinstance(obj, dict):
        try:
            obj = json.dumps(obj, default=str)
        except Exception:
            logger.critical(
                f"LOGURU EXCEPTION: safe_log parsing!!! "
                f"{traceback.format_exc()}"
            )
            raise
    curly_escape = obj.replace("{", "{{").replace("}", "}}")
    square_escape = curly_escape.replace("<", "\<").replace(">", "\>")
    return square_escape
