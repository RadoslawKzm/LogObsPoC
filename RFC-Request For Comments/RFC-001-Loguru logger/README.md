# RFC-001: Replace Built-in Logging with Loguru

- **RFC Number:** 001  
- **Title:** Replace Built-in Logging with Loguru  
- **Author:** Radek Kuźma  
- **Created:** 2025-07-15  
- **Updated:** 2025-07-15  
- **Status:** Accepted  
- **Discussion:** Not Applicable

---

## 🎯 Summary

Replace Python’s built-in `logging` module with Loguru for improved readability, structured log output, correlation ID tracking, better exception context, and custom levels and formatting. <br>
This RFC also introduces a centralized logger setup and utility functions to ensure consistent and safe logging practices.

---

## 🧩 Motivation

The default `logging` module is:

- Verbose and error-prone to configure
- Lacks rich formatting or structured logging without third-party add-ons
- Not async-friendly by default

Switching to Loguru provides:

- Simpler syntax (`logger.info()` instead of boilerplate logger setup)
- JSON + human-readable log outputs
- Custom log levels and colorization
- Built-in correlation ID tracking integration
- Automatic exception traceback logging and handling

---

## 🛠️ Detailed Design

### Configuration

We introduce a centralized `logger_setup()` function that:

- Removes all default Loguru sinks  
- Adds four sinks:  
  - `stderr` with colored human-readable logs (for dev)  
  - `logs/human_readable.log` for persisted human logs  
  - `logs/safe.json` for safe JSON serialized logs (no diagnostics)  
  - `logs/unsafe.json` for diagnostic JSON logs (more verbose)  
- Applies `correlation_id` filter on all logs for traceability  
- Defines custom log levels like `ENTER`, `EXIT`, `START`, `END 200`, etc.  

### Logging Utilities

- `safe_log(obj: str | dict) -> str`  
  - Parses dictionaries to avoid Loguru key errors on lazy logs  
  - Converts non-string/non-dict objects to string safely  
  - Escapes `{}` braces to avoid formatting issues  
- `correlation_id_filter(record: dict) -> bool`  
  - Injects current correlation ID into log records' extra fields  

### Logging Usage

- Use `logger.trace()`, to record fine-grained information about the program's execution path for diagnostic and analytics purposes. 
- Use `logger.debug()`, to record messages for debugging purposes. 
- Use `logger.info()`, to record informational messages that describe the normal operation of the program.
- Use `logger.success()`, to indicate the success of an operation.
- Use `logger.warning()`, to indicate an unusual event that may require further investigation.
- Use `logger.error()`, to record error conditions that affected a specific operation.
- Use `logger.exception()`, same as error but inside exception handlers to log tracebacks automatically  except Exception: **WITHOUT as exc** 
- Use `logger.critical()`, to record error conditions that prevent a core function from working.
- `.exception()` automatically adds **active** stack trace and exception info; `.error()` does not  
- Use `opt(lazy=True)` only on INFO and below. `logger.opt(lazy=True).debug("Message, {fnc}", fnc=lambda: expensive_func())`<br>
Python has to evaluate all fstrings before passing to loguru. <br>
Loguru will dismiss this log but processing by python is wasted.<br>
To avoid it, we trick python by providing lambda 0 cost and let loguru decide to evaluate or not.

---

## 🔁 Alternatives Considered

- Continue using built-in `logging` with manual configuration (complex, error-prone)  
- Use other structured loggers like structlog (more complex, less feature-rich)  
- Third-party logging middleware (less customizable, no built-in correlation ID support)  

---

## 🔄 Backward Compatibility

- Logging API changes minimally: `logger` replaces built-in logger  
- Existing logging calls must be updated to new logger instance and utilities  
- Old logging config is removed  

---

## 📈 Drawbacks

- Requires developers to learn Loguru API and new patterns  
- Possible confusion with lazy evaluation (`opt(lazy=True)`)  
- Slight increase in initial setup complexity  
- Must ensure `safe_log` used consistently with complex objects  

---

## ✅ Acceptance Criteria

- All backend code uses centralized `logger` instance from `loguru`  
- Logs include correlation IDs automatically  
- JSON and human-readable logs generated concurrently  
- Exception tracebacks logged with `.exception()` calls  
- No key errors from logging dicts or objects in production logs  
- Clear documentation on `safe_log` usage and lazy evaluation pitfalls  

---

## 🗒️ Unresolved Questions

- Should internal helper functions be wrapped to enforce safe logging patterns?  
- How to best train developers on Loguru idioms and safe usage?  

---

## 📚 References

- [Loguru GitHub](https://github.com/Delgan/loguru)  
- [Loguru Documentation](https://loguru.readthedocs.io/en/stable/)  
- Internal: `backend/loguru_logger.py`  

---

## ✅ Key Benefits

- **Simpler Syntax:** Less boilerplate, more expressive log calls  
- **Structured Logging:** JSON outputs alongside human-readable logs  
- **Correlation IDs:** Automatic inclusion for distributed tracing  
- **Custom Levels:** Domain-specific levels improve log clarity  
- **Safe Logging:** `safe_log` prevents common runtime errors with dicts and objects  
- **Better Tracebacks:** `.exception()` automatically logs detailed stack traces  
- **Concurrent Sinks:** Logs routed to multiple destinations with independent formats and retention policies  

> 🧠 Summary: Migrating to Loguru enhances log reliability, developer experience, and observability, positioning our backend for better debugging and monitoring at scale.

---

## ❓ FAQ

> Common questions about migrating to Loguru and logging best practices.

### Q: Why not always use `opt(lazy=True)` for performance?

**A:** Lazy evaluation defers log message formatting, which can improve performance if the message is never logged. <br>
Ensure lambda message won't break logging with unescaped JSON etc.

---

### Q: How does `logger.exception()` differ from `logger.error()`?

**A:** `logger.exception()` should be called inside an `except` block; it automatically logs the stack trace and exception info. `logger.error()` just logs the message without traceback.

---

### Q: Can we mix built-in logging and Loguru?

**A:** Technically yes, but not recommended. Mixing can cause inconsistent formats and missing correlation IDs. It's best to fully migrate to Loguru.

---

> Have a question? Ask it once and if recurring, it will be added here.

