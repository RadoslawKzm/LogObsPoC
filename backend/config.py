from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvType(str, Enum):
    LOCAL = "LOCAL"
    DEV = "DEV"
    PPD = "PPD"
    PROD = "PROD"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8765
    ENV_TYPE: EnvType = EnvType.LOCAL


settings = Settings()
