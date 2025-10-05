import time

import fastapi
from loguru import logger

from backend.auth import extract_jwt


def add_http_middleware(*, _app: fastapi.FastAPI):
    @_app.middleware("http")
    async def log_requests(request: fastapi.Request, call_next):
        request.state.user = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            request.state.user = await extract_jwt(token)
        http_version = request.scope.get("http_version")
        with logger.contextualize(
            user_agent=request.headers["user-agent"] or "",
            client_ip=request.client.host,
            http_version=http_version,
            method=request.method,
            path=request.url.path,
            user=request.state.user,
        ):
            logger.log(
                "ENTER",
                f"IN {request.method}:{request.url.path}",
            ),
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        msg = (
            f"OUT {request.method}:{request.url.path} | "
            f"{response.status_code} | {duration:.4f}s"
        )
        if 200 <= response.status_code <= 299:
            logger.log("EXIT 200", msg)
        elif 300 <= response.status_code <= 399:
            logger.log("EXIT 300", msg)
        elif 400 <= response.status_code <= 499:
            logger.log("EXIT 400", msg)
        else:  # 500++
            logger.log("EXIT 500", msg)
        return response
