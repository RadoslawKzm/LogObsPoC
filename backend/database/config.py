import pydantic_settings


class PostgresConfig(pydantic_settings.BaseSettings):
    POSTGRES_HOSTNAME: str = None
    POSTGRES_PORT: int = None
    POSTGRES_DB: str = None
    POSTGRES_USER: str = None
    POSTGRES_PASSWORD: str = None
    SYNC_DRIVER: str = "postgresql+psycopg2"
    ASYNC_DRIVER: str = "postgresql+asyncpg"

    # computed fields
    sync_url: str = "None"
    async_url: str = "None"

    def model_post_init(self, __context: dict) -> None:
        # automatically compute URLs after init
        self.sync_url = (
            f"{self.SYNC_DRIVER}://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOSTNAME}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        self.async_url = (
            f"{self.ASYNC_DRIVER}://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOSTNAME}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


pg_config = PostgresConfig()
