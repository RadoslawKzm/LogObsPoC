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
        ).info("HTTP request received")
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        logger.bind(
            method=request.method,
            path=request.url.path,
            response_code=response.status_code,
            duration=duration,
        ).info("HTTP request end of road".rstrip())
        return response
