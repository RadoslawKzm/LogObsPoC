from enum import Enum

from pydantic_settings import BaseSettings


class EnvType(str, Enum):
    LOCAL = "LOCAL"
    DEV = "DEV"
    PPD = "PPD"
    PROD = "PROD"


ENV_LOG_LEVEL_MAP: dict[EnvType, str] = {
    EnvType.LOCAL: "TRACE",
    EnvType.DEV: "DEBUG",
    EnvType.PPD: "INFO",
    EnvType.PROD: "INFO",
}


class Settings(BaseSettings):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8765
    ENV_TYPE: EnvType

    # ===== Postgres =====
    POSTGRES_HOSTNAME: str = None
    POSTGRES_PORT: int = None
    POSTGRES_DB: str = None
    POSTGRES_USER: str = None
    POSTGRES_PASSWORD: str = None
    POSTGRES_SYNC_DRIVER: str = "postgresql+psycopg2"
    POSTGRES_ASYNC_DRIVER: str = "postgresql+asyncpg"

    # computed fields
    sync_url: str = "None"
    async_url: str = "None"

    def model_post_init(self, __context: dict) -> None:
        # automatically compute URLs after init
        self.sync_url = (
            f"{self.POSTGRES_SYNC_DRIVER}://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOSTNAME}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        self.async_url = (
            f"{self.POSTGRES_ASYNC_DRIVER}://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOSTNAME}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # # ===== MongoDB =====
    # MONGO_USER: str = None
    # MONGO_PASSWORD: str = None
    # MONGO_HOSTNAME: str = None
    # MONGO_PORT: str = None
    # MONGO_DB: str = None

    # ===== RabbitMQ =====
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_VIRTUAL_HOST: str
    RABBITMQ_EXCHANGE: str
    RABBITMQ_S_QUEUE: str
    RABBITMQ_M_QUEUE: str
    RABBITMQ_L_QUEUE: str

    # Health check
    CGROUP_CPU_USAGE: str | None = None
    CGROUP_CPU_QUOTA: str | None = None
    CGROUP_CPU_PERIOD: str | None = None
    CGROUP_MEMORY_USAGE: str | None = None
    CGROUP_MEMORY_LIMIT: str | None = None

    @property
    def LOG_LEVEL(self) -> str | int:
        """Return the appropriate log level for the environment."""
        return ENV_LOG_LEVEL_MAP[self.ENV_TYPE]


settings = Settings()
