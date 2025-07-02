# from loguru import logger
#
# from .log_config import configs
#
#
# def logger_setup():
#     logger.remove()
#     for item in log_configs:
#         cfg = item["config"]
#         logger.add(
#             cfg.logs_path,
#             level=cfg.log_level,
#             format=cfg.format,
#             filter=cfg.filter,
#             rotation=cfg.rotation,
#             retention=cfg.retention,
#             enqueue=cfg.enqueue,
#             backtrace=cfg.backtrace,
#             diagnose=cfg.diagnose,
#             serialize=item.get("serialize", False),
#         )

# def setup_human_readable_console_logger():
#     """Setting up stdout logger with human-readable format"""
#     logger.add(
#         ConsoleHumanLogsConfig.logs_path,
#         level=ConsoleHumanLogsConfig.log_level,
#         format=ConsoleHumanLogsConfig.log_format,
#         filter=ConsoleHumanLogsConfig.log_filter,
#         enqueue=ConsoleHumanLogsConfig.enqueue,
#         backtrace=ConsoleHumanLogsConfig.backtrace,
#         diagnose=ConsoleHumanLogsConfig.diagnose,
#     )
#
#
# def setup_human_readable_file_logger():
#     """Setting up file output logger with human-readable format"""
#     logger.add(
#         FileHumanLogsConfig.logs_path,
#         level=FileHumanLogsConfig.log_level,
#         rotation=FileHumanLogsConfig.log_rotation,
#         retention=FileHumanLogsConfig.log_retention,
#         format=FileHumanLogsConfig.log_format,
#         filter=FileHumanLogsConfig.log_filter,
#         enqueue=FileHumanLogsConfig.enqueue,
#         backtrace=FileHumanLogsConfig.backtrace,
#         diagnose=FileHumanLogsConfig.diagnose,
#     )
#
#
# def setup_json_file_logger():
#     """Setting up JSON file logger (for Loki / structured logs)"""
#     logger.add(
#         SafeJsonFileLogsConfig.logs_path,
#         level=SafeJsonFileLogsConfig.log_level,
#         retention=SafeJsonFileLogsConfig.log_retention,
#         rotation=SafeJsonFileLogsConfig.log_retention,
#         format=SafeJsonFileLogsConfig.log_format,
#         filter=SafeJsonFileLogsConfig.log_filter,
#         enqueue=SafeJsonFileLogsConfig.enqueue,
#         backtrace=SafeJsonFileLogsConfig.backtrace,
#         diagnose=SafeJsonFileLogsConfig.diagnose,
#         serialize=True,  # ← this is what makes it JSON
#     )
#
#
# def setup_json_secrets_file_logger():
#     """Sensitive/verbose structured logs for internal diagnostics"""
#     logger.add(
#         UnsafeJsonFileLogsConfig.logs_path,
#         level=UnsafeJsonFileLogsConfig.log_level,
#         retention=UnsafeJsonFileLogsConfig.log_retention,
#         rotation=UnsafeJsonFileLogsConfig.log_retention,
#         format=UnsafeJsonFileLogsConfig.log_format,
#         filter=UnsafeJsonFileLogsConfig.log_filter,
#         enqueue=UnsafeJsonFileLogsConfig.enqueue,
#         backtrace=UnsafeJsonFileLogsConfig.backtrace,
#         diagnose=UnsafeJsonFileLogsConfig.diagnose,
#         serialize=True,
#     )


# def logger_setup():
#     logger.remove()
#     setup_human_readable_console_logger()
#     setup_human_readable_file_logger()


# flake8: noqa: E501
# TRACE (5): used to record fine-grained information about the program's execution path for diagnostic and analytics purposes.
# DEBUG (10): used by developers to record messages for debugging purposes.
# INFO (20): used to record informational messages that describe the normal operation of the program.
# SUCCESS (25): similar to INFO but used to indicate the success of an operation.
# WARNING (30): used to indicate an unusual event that may require further investigation.
# ERROR (40): used to record error conditions that affected a specific operation.
# CRITICAL (50): used to record error conditions that prevent a core function from working.
# flake8: noqa: enable
