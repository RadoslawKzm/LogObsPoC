import time

import fastapi
from loguru import logger


def add_http_middleware(*, app: fastapi.FastAPI):
    @app.middleware("http")
    async def log_requests(request: fastapi.Request, call_next):
        http_version = request.scope.get("http_version")
        logger.log(
            "ENTER",
            f"HTTP {http_version} Inbound: {request.client.host} | "
            f"{request.method} {request.url.path}",
        )
        logger.debug(f"Headers: {request.headers}")
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        msg = (
            f"HTTP Outbound- {request.method} {request.url.path} | "
            f"{response.status_code} {duration:.3f}s"
        )
        if 200 <= response.status_code < 299:
            with logger.contextualize(
                method=request.method,
                path=request.url.path,
                response_code=response.status_code,
                duration=duration,
            ):
                logger.log("EXIT", msg)
        return response
