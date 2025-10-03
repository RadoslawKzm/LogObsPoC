from enum import Enum

from pydantic_settings import BaseSettings


class EnvType(str, Enum):
    LOCAL = "LOCAL"
    DEV = "DEV"
    PPD = "PPD"
    PROD = "PROD"


ENV_LOG_LEVEL_MAP: dict[EnvType, str] = {
    EnvType.LOCAL: "TRACE",
    EnvType.DEV: "TRACE",
    EnvType.PPD: "TRACE",
    EnvType.PROD: "INFO",
}


class SettingsWorker(BaseSettings):
    # ===== Api =====
    WORKER_API_HOST: str = "0.0.0.0"
    WORKER_API_PORT: int = 8000
    WORKER_RABBIT_QUEUE: str
    ENV_TYPE: EnvType

    # ===== RabbitMQ =====
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_PREFETCH_COUNT: int
    RABBITMQ_VIRTUAL_HOST: str

    # ===== Health check =====
    CGROUP_CPU_USAGE: str | None = None
    CGROUP_CPU_QUOTA: str | None = None
    CGROUP_CPU_PERIOD: str | None = None
    CGROUP_MEMORY_USAGE: str | None = None
    CGROUP_MEMORY_LIMIT: str | None = None

    @property
    def LOG_LEVEL(self) -> str | int:
        """Return the appropriate log level for the environment."""
        return ENV_LOG_LEVEL_MAP[self.ENV_TYPE]


worker_settings = SettingsWorker()
