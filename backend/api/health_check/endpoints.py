import random
import time

import fastapi
import psutil
from loguru import logger

from . import response_examples

health_router = fastapi.APIRouter(prefix="/health-app", tags=["health-app"])


@health_router.get(
    "/",
    status_code=200,
    responses=response_examples.response_200,
)
async def health() -> dict:
    log_host_cpu_load()
    log_host_memory_load()
    log_host_disk_io()
    log_host_net_io()
    # log_container_cpu_usage()
    # log_container_memory_usage()
    responses = [
        "I am Groot",
        "This is the way",
        "Luke, I am your father",
        "Hodor...",
    ]
    return {"data": random.choice(responses)}


def log_host_cpu_load():
    cpu_percent = psutil.cpu_percent(interval=None)
    logger.opt(lazy=True).trace(
        "Host CPU usage: {cpu:.2f}%",
        cpu=lambda: psutil.cpu_percent(interval=None),
    )
    return cpu_percent


def log_host_memory_load() -> None:
    mem = psutil.virtual_memory()
    logger.opt(lazy=True).trace(
        "Host memory usage: {used:.2f} / {total:.2f} GB ({percent:.2f}%)",
        used=lambda: mem.used / (1024**3),
        total=lambda: mem.total / (1024**3),
        percent=lambda: mem.percent,
    )


def log_host_disk_io() -> None:
    io = psutil.disk_io_counters()
    logger.opt(lazy=True).trace(
        "Host disk IO: read {read_mb:.2f} MB, write {write_mb:.2f} MB",
        read_mb=lambda: io.read_bytes / (1024**2),
        write_mb=lambda: io.write_bytes / (1024**2),
    )


def log_host_net_io() -> None:
    net = psutil.net_io_counters()
    logger.opt(lazy=True).trace(
        "Host network IO: sent {sent_mb:.2f} MB, received {recv_mb:.2f} MB",
        sent_mb=lambda: net.bytes_sent / (1024**2),
        recv_mb=lambda: net.bytes_recv / (1024**2),
    )


def _get_prev_times(
    *, now: float, usage_ns: float
) -> tuple[float, ...] | None:
    prev_time = previous_state["time"]
    prev_usage_ns = previous_state["usage_ns"]

    # First call: store and return None
    if prev_time is None or prev_usage_ns is None:
        previous_state["time"] = now
        previous_state["usage_ns"] = usage_ns
        logger.debug("Initial CPU usage reading, waiting for next sample.")
        return None
    return prev_time, prev_usage_ns


def read_cgroup(path: str) -> int:
    with open(path) as f:
        return int(f.read().strip())


# Store previous state between calls
previous_state: dict[str, float | None] = {"time": None, "usage_ns": None}


def log_container_cpu_usage() -> None:
    # total ns used by container
    usage_ns = read_cgroup("/sys/fs/cgroup/cpu/cpuacct.usage")
    now = time.time()  # current wall-clock time in seconds
    try:
        prev_time, prev_usage_ns = _get_prev_times(now=now, usage_ns=usage_ns)
    except TypeError:
        return None

    # Calculate deltas
    delta_time = now - prev_time
    delta_usage = usage_ns - prev_usage_ns

    if delta_time <= 0:
        logger.warning("Non-positive delta time detected.")
        return None

    # Get number of CPUs available to the container (optional but recommended)
    try:
        cpu_quota = int(read_cgroup("/sys/fs/cgroup/cpu/cpu.cfs_quota_us"))
        cpu_period = int(read_cgroup("/sys/fs/cgroup/cpu/cpu.cfs_period_us"))
    except Exception as exc_info:
        logger.warning(f"Failed to read CPU quota info: {exc_info}")
        return None
    # Convert nanoseconds to seconds, then calculate usage %
    cpu_count = cpu_quota / cpu_period
    cpu_percent = (delta_usage / 1e9) / delta_time * 100 / cpu_count
    logger.opt(lazy=True).trace(
        "Container CPU usage: {cpu:.2f}%",
        cpu=lambda: cpu_percent,
    )
    # Save current state for next sample
    previous_state["time"] = now
    previous_state["usage_ns"] = usage_ns


def log_container_memory_usage() -> None:
    usage = read_cgroup("/sys/fs/cgroup/memory/memory.usage_in_bytes")
    limit = read_cgroup("/sys/fs/cgroup/memory/memory.limit_in_bytes")
    percent = (usage / limit) * 100 if limit > 0 else 0
    logger.opt(lazy=True).trace(
        "Container memory usage: {used:.2f} / {limit:.2f} GB ({percent:.2f}%)",
        used=lambda: usage / (1024**3),
        limit=lambda: limit / (1024**3),
        percent=lambda: percent,
    )
