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

#
# # class MongoConfig(pydantic_settings.BaseSettings):
# #     MONGO_USER: str = None
# #     MONGO_PASSWORD: str = None
# #     MONGO_HOSTNAME: str = None
# #     MONGO_PORT: str = None
# #     MONGO_DB: str = None
#
#     # model_config = pydantic_settings.SettingsConfigDict(
#     #     env_file=CURRENT_FILE / "deployment/.env",
#     #     env_file_encoding="utf-8",
#     #     extra="ignore",
#     # )
#
#
# # class RabbitConfig(pydantic_settings.BaseSettings):
# #     model_config = pydantic_settings.SettingsConfigDict(
# #         env_file=(
# #             BASE_DIR / ".env",  # shared across backend
# #             pathlib.Path(__file__).parent
# #             / ".env",  # module-specific overrides
# #         ),
# #         env_file_encoding="utf-8",
# #         case_sensitive=False,
# #     )
# #     RABBITMQ_HOST: str
# #     RABBITMQ_PORT: int
# #     RABBITMQ_USER: str
# #     RABBITMQ_PASSWORD: str
# #     RABBITMQ_VIRTUAL_HOST: str
# #     RABBITMQ_EXCHANGE: str
# #     RABBITMQ_S_QUEUE: str
# #     RABBITMQ_M_QUEUE: str
# #     RABBITMQ_L_QUEUE: str
# #     RABBITMQ_PREFETCH_COUNT: int
#
pg_config = PostgresConfig()
# # rabbit_config = RabbitConfig()
# # mongo_config = MongoConfig()
