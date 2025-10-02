import fastapi
from loguru import logger
import psutil
import time

from backend.api.config import settings

health_router = fastapi.APIRouter(prefix="/health-app", tags=["health-app"])

def get_cgroup_usage(*, path: str) -> int:
    """Reads a cgroup metric from the specified file."""
    if not path:
        return False
    try:
        with open(path) as f:
            return int(f.read().strip())
    except Exception as e:
        logger.error(f"Failed to read cgroup value from {path}: {e}")
        raise


PREVIOUS_STATE: dict = {
    "time": time.time(),
    "usage_ns": get_cgroup_usage(path=settings.CGROUP_CPU_USAGE),
}


def container_cpu_usage() -> tuple:
    """Logs the container CPU usage."""
    prev_time = PREVIOUS_STATE["time"]
    prev_usage_ns = PREVIOUS_STATE["usage_ns"]
    usage_ns = get_cgroup_usage(path=settings.CGROUP_CPU_USAGE)
    now = time.time()

    delta_time = now - prev_time
    delta_usage = usage_ns - prev_usage_ns

    cpu_quota = get_cgroup_usage(path=settings.CGROUP_CPU_QUOTA)
    cpu_period = get_cgroup_usage(path=settings.CGROUP_CPU_PERIOD)
    # if cpu_quota <= 0 or cpu_period <= 0:
    #     logger.warning("Unable to calculate CPU core count.")
    #     return None
    cpu_core_count = cpu_quota / cpu_period
    cpu_percent = (delta_usage / 1e9) / delta_time * 100 / cpu_core_count
    # if not cpu_percent:
    #     logger.warning("Unable to calculate CPU usage percentage.")
    #     return None
    PREVIOUS_STATE["time"] = now
    PREVIOUS_STATE["usage_ns"] = usage_ns
    return cpu_percent, cpu_core_count


def container_ram_usage():
    ram_usage = get_cgroup_usage(path=settings.CGROUP_MEMORY_USAGE)
    total_ram = get_cgroup_usage(path=settings.CGROUP_MEMORY_LIMIT)
    ram_percentage = (ram_usage / total_ram) * 100 if total_ram > 0 else 0
    return ram_percentage, ram_usage, total_ram


def container_stats():
    if not is_container():
        return False
    cpu_percent, cpu_core_count = container_cpu_usage()
    cpu_core_usage = cpu_percent * cpu_core_count / 100
    logger.opt(lazy=True).trace(
        "Container CPU usage: {percent:.2f}% {used:.2f}/{total:.2f} Cores",
        percent=lambda: cpu_percent,
        used=lambda: cpu_core_count,
        total=lambda: cpu_core_usage,
    )
    # ----- Container Memory Usage -----
    ram_percentage, ram_usage, total_ram = container_ram_usage()
    logger.opt(lazy=True).trace(
        "Container RAM usage: {percent:.2f}% {usage:.2f}/{total:.2f} GB",
        percent=lambda: ram_percentage,
        usage=lambda: ram_usage / (1024**3),
        total=lambda: total_ram / (1024**3),
    )
    return {
        "CPU": {
            "percentage": cpu_percent,
            "cores_used": cpu_core_usage,
            "cores_total": cpu_core_count,
        },
        "RAM": {
            "percentage": ram_percentage,
            "used": ram_usage,
            "total": total_ram,
        },
    }


def is_container():
    try:
        container = get_cgroup_usage(path=settings.CGROUP_CPU_USAGE)
        if not container:
            return False
        return True
    except Exception as e:
        return False


@health_router.get("/", status_code=200)
async def health() -> dict:
    # ----- Host CPU Usage -----
    host_cpu_percentage = psutil.cpu_percent(interval=None)
    host_cpu_count = psutil.cpu_count()
    host_cpu_core_usage = host_cpu_percentage * host_cpu_count / 100
    logger.opt(lazy=True).trace(
        "Host CPU usage: {percent:.2f}% {used:.2f}/{total:.2f} Cores",
        percent=lambda: host_cpu_percentage,
        used=lambda: host_cpu_core_usage,
        total=lambda: host_cpu_count,
    )
    # ----- Host Memory Usage -----
    host_ram_load = psutil.virtual_memory()
    logger.opt(lazy=True).trace(
        "Host memory usage: {percent:.2f}% {used:.2f}/{total:.2f} GB",
        used=lambda: host_ram_load.used / (1024**3),
        total=lambda: host_ram_load.total / (1024**3),
        percent=lambda: host_ram_load.percent,
    )
    # ----- Container Usage -----
    container = container_stats()
    return {
        "host": {
            "CPU": {
                "percentage": host_cpu_percentage,
                "cores_used": host_cpu_core_usage,
                "cores_total": host_cpu_count,
            },
            "RAM": {
                "percentage": host_ram_load.percent,
                "used": round(host_ram_load.used / (1024**3), 2),
                "total": host_ram_load.total / (1024**3),
            },
        },
        "container": container,
    }


@health_router.get("/rabbit", status_code=200)
async def rabbit(request: fastapi.Request) -> dict:
    """Report RabbitMQ connection health using app.state-stored objects."""
    conn = getattr(request.app.state, "rabbit_connection", None)
    ch = getattr(request.app.state, "rabbit_channel", None)
    if not conn or ch:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Problem with RabbitMQ"},
        )
    if conn.is_closed or ch.is_closed:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Not connected to RabbitMQ"},
        )
    return {"status": "healthy", "message": "Connected to RabbitMQ"}

