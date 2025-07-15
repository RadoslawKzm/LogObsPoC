# RFC-002: Centralized Exception Handlers and Error Taxonomy

- **RFC Number:** 002  
- **Title:** Centralized Exception Handlers and Error Taxonomy  
- **Author:** Radek Kuźma  
- **Created:** 2025-07-15  
- **Updated:** 2025-07-15  
- **Status:** Accepted  
- **Discussion:** Not Applicable

---

## 🎯 Summary

Introduce a structured exception handling system using custom error classes grouped by domain (API, DB, Cloud, etc.), with centralized FastAPI exception handlers and internal error codes. This avoids scattered `try/except` blocks and standardizes logging, response format, and traceability.

---

## 🧩 Motivation

Currently, error handling is inconsistent. Developers must:
- Remember to wrap logic in `try/except`
- Manually log errors
- Manually raise `HTTPException`
- Duplicate effort when error messaging/logging changes

This RFC eliminates that repetition by providing:
- A unified `add_exception_handlers()` function
- Domain-specific exception trees (`ApiError`, `DbError`, etc.)
- One-liner raising (`raise ForbiddenError()` instead of verbose blocks)
- Centralized log formatting
- Internal traceable error codes in logs and structured markdown

---

## 🛠️ Detailed Design

- All exceptions inherit from `BaseCustomError`, which provides:
  - `http_code`
  - `external_message`
  - `internal_message`
  - `internal_code`
- Exception domains (API, DB, Cloud, etc.) live in separate files following hexagonal architecture
- `add_exception_handlers()` is called once in `main.py` or app init
- Each handler logs:
  - Traceback (safely)
  - Internal code and messages
  - HTTP response code
- Errors are logged via `loguru` and returned in JSON like:
  ```json
  {
    "message": "You are not authorized."
  }
  ```
- Internal error codes are fully documented in `internal_codes.md`

---

## 🔁 Alternatives Considered

- Using only built-in `HTTPException` and manual try/catch per feature (verbose and error-prone)
- Relying on third-party exception middleware (too generic, no domain classification)
- Pydantic error wrapping (only handles input validation, not business logic)

---

## 🔄 Backward Compatibility

Fully backward-compatible:
- Legacy code using `raise HTTPException(...)` still works
- New system is opt-in per feature/module
- Over time, teams can migrate module-by-module

---

## 📈 Drawbacks

- Adds some boilerplate for defining new exceptions
- Developers must remember to raise domain-specific exceptions instead of generic ones
- If abused (e.g., adding too many similar error classes), system can bloat

---

## ✅ Acceptance Criteria

- Application installs centralized exception handlers
- Logs contain structured tracebacks + internal codes
- 100% of known handled API/DB errors are raised from custom exceptions
- `internal_codes.md` is updated and serves as the source of truth
- No more inline `try/except` + `logger.error` + `raise HTTPException` in API code

---

## 🗒️ Unresolved Questions

- Should internal codes be returned in debug mode for easier frontend integration?
- Do we version or tag internal codes in the future?

---

## 📚 References

- [FastAPI Exception Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [Loguru Logging](https://github.com/Delgan/loguru)
- [HTTP RFCs](https://www.rfc-editor.org/)
- Internal: `backend/api/v2/exceptions/`, `internal_codes.md`

---

## ✅ Key Benefits

- **Single Responsibility:** Logging, traceback, response construction are decoupled from business logic.
- **DRY:** No repeated logging/response logic per endpoint.
- **Traceability:** Internal codes map to documented causes.
- **Extensibility:** Easy to add new error domains (e.g., `cloud_exceptions.py`)
- **Security:** External users see only sanitized messages.
- **Consistency:** All errors use uniform structure for logs and client output.
- **Maintainability:** Changing error behavior (e.g., wording, logging, status codes) is centralized.

> 🧠 Summary: This system makes our error handling declarative, safe, auditable, and scalable—aligned with clean architecture principles.

---

## ❓ FAQ

> Common developer questions about this RFC. Refer here before opening new discussions.

### Q: Why not just use FastAPI's `HTTPException` everywhere?

**A:** `HTTPException` is low-level and requires manually repeating the same message, status code, and logging for every use. <br>
With our pattern, you just `raise ForbiddenError()` and everything else is handled: logging, formatting, code tracing, and client response.

---

### Q: How do I define a new exception?

**A:** Subclass the appropriate base like `ApiError` or `DbError`, and define:

```python
class MyNewError(ApiError):
    http_code = 400
    external_message = "Bad request."
    internal_code = 1999
    internal_message = "Client sent malformed data."
```

Then just `raise MyNewError()` in your logic.
Don't forget to add internal_codes.md entry :)

---

### Q: Can we include the internal error code in the JSON response?

**A:** No, by default it's hidden for security reasons. <br>
If needed (e.g., in dev/staging), we can optionally expose it under a `DEBUG` flag.

---

### Q: I got an error, but it doesn’t map to any known internal code — what do I do?

**A:** Wrap it in a custom error or raise `UnknownServerError` for now. <br>
Then open a PR to define a proper code and explanation in `internal_codes.md`.

---

> Have a new question? Ask it once — if it's recurring, we’ll add it here.
