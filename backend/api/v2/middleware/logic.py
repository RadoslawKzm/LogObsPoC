import time

import fastapi
from loguru import logger


def add_http_middleware(*, app: fastapi.FastAPI):
    @app.middleware("http")
    async def log_requests(request: fastapi.Request, call_next):
        logger.bind(
            user_agent=request.headers["user-agent"] or "",
            client_ip=request.client.host,
            http_version=request.scope.get("http_version"),
            method=request.method,
            path=request.url.path,
        ).log("ENTER", f"HTTP Inbound-V2 {request.method} {request.url.path}")
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        log_obj = logger.bind(
            method=request.method,
            path=request.url.path,
            response_code=response.status_code,
            duration=duration,
        )
        msg = (
            f"HTTP Outbound-V2 {request.method} {request.url.path} | "
            f"{response.status_code} {duration:.3f}s"
        )
        if 200 <= response.status_code < 299:
            log_obj.log("EXIT", msg)
        return response
