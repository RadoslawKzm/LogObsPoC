from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


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
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8765
    ENV_TYPE: EnvType = EnvType.LOCAL

    @property
    def LOG_LEVEL(self) -> str | int:
        """Return appropriate log level for the environment."""
        return ENV_LOG_LEVEL_MAP[self.ENV_TYPE]


settings = Settings()
