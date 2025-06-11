# FastAPI Project Improvement Suggestions

## Table of Contents

- [1. ASGI Traceability with asgi-correlation-id](#1-asgi-traceability-with-asgi-correlation-id)
  - [🧠 The Problem](#-the-problem)
  - [✅ Benefits of ASGI Correlation IDs](#-benefits-of-asgi-correlation-ids)
- [2. Custom exceptions](#2-custom-exceptions)
  - [Pros from this approach](#pros-from-this-approach)
- [3. Unified and Powerful Logging with **Loguru**](#3-unified-and-powerful-logging-with-loguru)
- [4. Centralized Exception Handling with FastAPI](#4-centralized-exception-handling-with-fastapi)
- [5. Clean Database Error Handling with Custom DbManager](#5-clean-database-error-handling-with-custom-dbmanager)
- [6. Built for Observability: Prometheus, Loki, Grafana Ready](#6-built-for-observability-prometheus-loki-grafana-ready)


## 1. ASGI Traceability with asgi-correlation-id
### 🧠 The Problem:
In asynchronous applications like FastAPI, requests can be interleaved due to await calls.  
That means multiple requests are processed concurrently and their logs become interwoven in the console or logging system.  
This makes it extremely difficult to trace logs belonging to a single request - especially under load.

Before (typical FastAPI logs):
```
INFO    ... project.views  This is an info log
WARNING ... project.models This is a warning log
INFO    ... project.views  This is an info log
INFO    ... project.views  This is an info log
WARNING ... project.models This is a warning log
WARNING ... project.models This is a warning log
```
After (with asgi-correlation-id):
```
INFO    ... [773fa6885] project.views  This is an info log
WARNING ... [773fa6885] project.models This is a warning log
INFO    ... [0d1c3919e] project.views  This is an info log
INFO    ... [99d44111e] project.views  This is an info log
WARNING ... [0d1c3919e] project.models This is a warning log
WARNING ... [99d44111e] project.models This is a warning log
```

Each request now has a correlation ID - a lightweight, unique identifier that traces a request across the entire stack.
### ✅ Benefits of ASGI Correlation IDs

#### 🔍 Easier Debugging Across Async Code
- Instantly filter logs related to a specific request or error - even in high-concurrency environments.
- No more jumping between unrelated log lines trying to reconstruct the request timeline.  

#### 📈 Improved Observability
- Works seamlessly with log aggregators like ELK, Loki, Datadog, or Sentry - enabling correlation of logs with metrics and traces.
- Paves the way for distributed tracing if/when you add tools like OpenTelemetry or Jaeger.

#### 💬 Better Support & Incident Response
- Correlation IDs can be exposed in API responses or error logs. When users report an issue, you can ask for the request ID and instantly find all related logs.
- Greatly speeds up triage and resolution times.

#### 🛠️ Low Overhead, High ROI
- Integration is simple: add middleware and adjust log formatter.
- No changes to business logic required - just works transparently for every incoming request.

#### 📦 Standardization
- Adds structure to logs, making them machine-readable and ready for future automation (e.g., alerting on slow or failed request patterns). 

#### 🌐 Readiness for Microservices / Serverless
- Essential for multi-service environments where tracing a request end-to-end is otherwise nearly impossible.
- Sets the stage for correlation across HTTP services, Kafka messages, background tasks, etc.

#### 🔐 Optional Privacy & Compliance Benefit
- Correlation IDs are opaque - they don't leak user or request data, making them safe for use in logs even in GDPR/PII-sensitive systems.

## 2. Custom exceptions.
We can prepare exceptions beforehand to be used in code.  
Instead of doing:

```python
try:
    x = find_id_in_db(id=1)
except some_db_error:
    raise fastapi.HTTPException(status_code=404, detail="Requested id is not present")
```
We can have:
```python
class RecordNotFound(DeveloperRisenException):
    http_code = fastapi.status.HTTP_404_NOT_FOUND
    external_message = "Record not found."
    internal_code = 21101
    internal_message = "Record not found in the database."
```
```python
def find_id_in_db(id:int):
    result = db.get(id=1)
    if not result:
        raise RecordNotFound(internal_message=f"Requested id={id} not found.")

x = find_id_in_db(id=1)
```
### Pros from this approach:

#### 🛠️ Improved Developer Experience (DX)  
- Clear and reusable exception classes reduce boilerplate code.
- Easier onboarding: New developers can quickly understand and use standardized error classes.
- Faster debugging with structured internal messages and codes.  
  
#### 📊 Better Observability and Monitoring
- Each exception has an internal_code - making it easy to track specific failure modes in logs, alerts, or dashboards.
- Integrates cleanly with observability platforms (e.g., Sentry, Grafana, Prometheus) by tagging exceptions by internal_code or type.

#### 🔐 Security by Design
- Clear separation of internal (developer-facing) and external (user-facing) messages ensures no sensitive data leaks in production.
- Avoids accidentally exposing stack traces or implementation details to users or attackers.

#### 📦 Centralized Control and Governance
- All exception behavior (HTTP codes, messages, logging level) is defined in one place.
- Easier audits and compliance checks for how the app handles errors.

#### 📈 Business Impact: Predictable and Consistent APIs
- APIs fail consistently and predictably, making it easier for frontend and partner systems to handle errors gracefully.
- If error responses follow a consistent shape and format, documentation becomes cleaner and integrations more stable.

#### 🚀 Scalability of Error Management
- As the application grows, new error types can be added easily without rewriting business logic or duplicating try/except blocks.
- Great foundation for future improvements like internationalization (i18n) of external messages.

🧪 Testability
- More testable code: easier to write unit tests that check for specific exceptions without relying on fragile string matching.
- Custom exceptions can also carry extra context useful during tests (e.g., the internal_code or internal_message).

📘 Documentation and Self-Service
- internal_code opens doors for auto-generating developer-friendly docs or internal wikis mapping each code to cause and solution.
- Can improve support team productivity when diagnosing production issues using error codes.
- Can expose internal_code to internal clients to faster fine-grained bug reports.

## 3. Unified and Powerful Logging with **Loguru**

### 🧠 The Problem:
Python's built-in `logging` module is powerful but:
- Verbose and hard to configure,
- Lacks built-in features like log rotation or structured formatting,
- Is not developer-friendly for modern async applications like FastAPI.

As a result, logs are often underutilized, inconsistent, or hard to read/maintain.

---

### ✅ Benefits of Using Loguru as the Default Logger

#### ⚡ Simpler, More Intuitive Logging
- Loguru is ready to use out of the box - no boilerplate or handler setup required.
- One-liner setup for common use cases:
```python
from loguru import logger
logger.info("Hello, Loguru!")
```

#### 🚨 Automatic Exception Logging
- Automatically captures and formats exceptions, including tracebacks:
```python
try:
1 / 0
except Exception:
logger.exception("Something went wrong!")
```

#### 🎨 Enhanced, Readable Formatting
- Beautiful, colorized logs by default - makes debugging in dev environments more pleasant.
- Configurable formatting for timestamps, levels, context, and more:
```
2025-06-11 12:45:21.482 | INFO | myapp.api:handler:23 - Incoming request: /items/1
```

#### 🌀 Built-in Async Support
- Fully compatible with async applications - logs inside `async def` behave predictably.
- No risk of context loss in concurrent execution.

#### 📦 Contextual Logging Made Easy
- Add request or user context with `logger.bind(...)`:
```python
logger.bind(user_id="abc123").info("User logged in")
```
- Works seamlessly with ASGI middleware to inject correlation IDs, user info, etc.

#### 🔁 Easy Log Rotation & Retention
- Built-in file rotation and retention policies with zero config overhead:
```python
logger.add("logs/app.log", rotation="1 week", retention="1 month", compression="zip")
```

#### 🔧 Built-in Sink Management
- Log to multiple destinations (files, stderr, remote API, Slack, etc.) in a few lines:
```python
logger.add("errors.json", level="ERROR", serialize=True)
```

#### 🚀 Better Performance
- Optimized for speed and low overhead - suitable for high-throughput APIs.
- Async-friendly I/O handling keeps the event loop unblocked.

---

### 📈 Result:
By standardizing on Loguru:
- We reduce developer friction when working with logs,
- Gain powerful features without extra dependencies or boilerplate,
- Improve the quality, consistency, and actionability of logs across the project.

## 4. Centralized Exception Handling with FastAPI

### 🧠 The Problem:
In complex systems, exceptions can:
- Leak internal details if not handled correctly,
- Be inconsistently formatted across endpoints,
- Result in unreadable logs or vague error messages for users,
- Require repeated boilerplate like `try/except` in every route.

We already introduced **custom exception classes** - now it's time to make them even more powerful using **FastAPI's exception handlers**.

---

### ✅ Benefits of Centralized Exception Handling

#### 🧩 Works Hand-in-Hand with Custom Exceptions
- Each exception type (`ApiException`, `DbException`, etc.) can be mapped to a precise response.
- Exception logic is *defined once* and applies *everywhere* - automatic, clean, and scalable.

#### 🛠️ Clean Separation of Internal vs External Concerns
- Internal logs contain rich technical details (error code, message, traceback).
- External responses return only safe, user-facing messages - no leaks, no confusion.

#### 📉 Less Boilerplate in Business Logic
Before:
```python
try:
find_user(id)
except DatabaseError:
raise HTTPException(404, "Not found")
```
After:
```python
user = find_user(id) # If it fails, exception handler takes care of everything
```

#### 🚨 Automatic Logging with Context
- Each handler logs structured details using **Loguru**:
```python
logger.opt(lazy=True, exception=exc).error(
    lambda: f"Internal message: {exc.internal_message}, "
    f"Internal code: {exc.internal_code}"
)
```

#### 💡 Customizable by Exception Type
- You can define different behavior per exception - including logging level, response headers, retry hints, etc.
- Example from our app:
```python
@app.exception_handler(api_exceptions.ApiException)
async def api_exception_handler(...): ...
```

#### 🔒 Safe Defaults for Unknown Exceptions
- A fallback `Exception` handler catches anything uncaught and returns a **safe**, generic error to users:
```python
return JSONResponse(
status_code=500,
content={"message": "Team got notified and working on solution."}
)
```

#### 📦 Fully Centralized Setup
- Handlers are added in **one place** with a helper:
```python
def add_exception_handlers(app: FastAPI) -> FastAPI:
...
return app
```

---

### 💡 Result
By combining:
- Custom exception classes (with internal and external messaging), and
- Exception handlers tailored to those classes,

we achieve:
- Clean API responses,
- Developer-friendly logs,
- Strong observability,
- Reduced clutter in business logic,
- **A single source of truth for all error handling**.

This is a foundational step toward production-grade reliability and maintainability.

## 5. Clean Database Error Handling with Custom DbManager

### 💡 Why This Matters
With our exception system and FastAPI handlers in place, we can now build powerful tools **on top** - like a custom `DbManager` that:
- Automatically handles transactions,
- Converts low-level SQLAlchemy errors into rich, structured exceptions,
- Keeps business logic clean, async-safe, and exception-resilient.

---

### ✅ What `DbManager` Does

```python
async with DbManager(database=DB) as session:
session.add(user)
```
or as Depends in FastAPI:
```python
@router.post("/users/")
async def create_user(
    user_data: UserCreate,
    session=Depends(DbManager.get_session),
):
    session.add(user_data)
```

This one line gives you:
- ✅ Automatic commit or rollback
- ✅ Clean session management (open, close, dispose)
- ✅ Structured error logging via **Loguru**
- ✅ Fine-grained exception translation

---

### 🔄 How It Works with Exception Handlers

Our `DbManager` converts raw SQLAlchemy exceptions into **custom exceptions**, like:

```python
raise db_exceptions.RecordNotFound()
```

Then, our FastAPI exception handlers catch and format those automatically:

```python
@app.exception_handler(db_exceptions.DbException)
async def db_exception_handler(
    request: Request,
    exc: db_exceptions.DbException,
) -> fastapi.responses.JSONResponse:
    logger.opt(lazy=True, exception=exc).error(
        lambda: f"Internal message: {exc.internal_message}, "
        f"Internal code: {exc.internal_code}"
    )
    return fastapi.responses.JSONResponse(
        status_code=exc.http_code,
        content={"message": exc.external_message},
    )

```

---

### ✨ Benefits

- **Business logic stays clean** - no `try/except`, no commit/rollback clutter.
- **Developers work with one abstraction** - `DbManager` just works.
- **No lost errors** - all DB issues are logged, traced, and surfaced through handlers.
- **Zero repetition** - exception mapping logic is centralized and consistent.
- **Safe suppression** is supported with `suppress_exc=True` for batch-like operations.

---

### 🔐 Example Use in Endpoint

```python
@router.post("/users/")
async def create_user(
    user_data: UserCreate,
    session=Depends(DbManager.get_session),
):
    user = User(**user_data.dict())
    session.add(user)
    return {"message": "User created"}

```

If anything goes wrong - unique constraint, connection loss, bad data - the correct error is raised, logged, and safely formatted for the API user.

---

### 🧱 Foundation for More
This pattern opens the door for:
- Retry-on-deadlock logic,
- Performance metrics (timing per transaction),
- Observability (e.g. OpenTelemetry spans),
- Background job DB operations with graceful failure fallback.

---

### 🧬 In Summary
Our custom `DbManager` wouldn't be possible without:
1. **Structured exception classes** to map errors,
2. **FastAPI handlers** to catch them cleanly,
3. **Loguru** for precise and lazy logging.

The result is a production-ready DB layer that's **clean for devs**, **safe for users**, and **easy to operate**.


## 6. Built for Observability: Prometheus, Loki, Grafana Ready

### 🔭 Why Observability Matters
As we grow, it's crucial to:
- **Track performance metrics**
- **Visualize failures**
- **Analyze system health over time**

Our current foundation (Loguru + structured exceptions + `DbManager`) is already setting us up for **deep integration** with:
- **Prometheus** for time-series metrics
- **Grafana** for dashboarding
- **Loki** for powerful structured log search

---

### 📈 Prometheus Timing Integration

Thanks to `DbManager` and centralized exception handlers, we can easily wrap operations with timing:

```python
import time

start = time.monotonic()
try:
async with DbManager(database=DB) as session:
...
finally:
duration = time.monotonic() - start
prometheus_metrics.db_transaction_time.observe(duration)
```

Or globally with a decorator or middleware!

---

### 📊 Structured Logging for Loki

Because all exceptions and logs follow a **structured format** (`internal_message`, `internal_code`, etc.), we can:
- Easily filter logs in Grafana Loki
- Group by error type, user action, or endpoint
- Spot trends like repeated integrity errors or slow queries

Example Loguru output:

```json
{
"level": "error",
"message": "DB IntegrityError",
"internal_code": "db.duplicate_user",
"http_code": 400,
"path": "/users/",
"duration_ms": 231
}
```

---

### 📉 Grafana Dashboards from Logs + Metrics

With this setup, dashboards become easy:
- 🔥 Slowest DB transactions
- ❌ Most frequent API errors
- 🧑💻 Failing endpoints by user activity
- ⏱️ Duration histograms for background jobs or specific endpoints

---

### 🔐 Secure and Context-Rich Logs

Since we're already adding context (like internal codes and error messages), we get:
- ✅ Developer insights (with `internal_message`)
- ✅ Safe public messages (via `external_message`)
- ✅ Consistent log format across DB, API, and generic errors

---

### 🧬 Summary: Ready for Scale and Insight

By putting in the structure now:
- We avoid spaghetti logs and one-off metrics later
- We unlock powerful dashboards without rewriting code
- We debug and improve with confidence

Your team will be able to **trace a spike in response times**, drill into **which DB queries failed**, and **correlate logs with metrics** - all without changes to business logic.

```
Logs go to Loki. Metrics go to Prometheus.
Everything is traceable in Grafana.
```

> ✅ Observability isn't an afterthought - it's built in from day one.
