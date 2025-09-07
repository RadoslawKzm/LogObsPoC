import pathlib
import pydantic_settings

CURRENT_FILE = pathlib.Path(__file__).parent.parent.parent


class PostgresConfig(pydantic_settings.BaseSettings):
    HOST: str = "localhost"
    POSTGRES_EXPOSE_PORT: int = None
    POSTGRES_DB: str = None
    POSTGRES_USER: str = None
    POSTGRES_PASSWORD: str = None
    SYNC_DRIVER: str = "postgresql+psycopg2"
    ASYNC_DRIVER: str = "postgresql+asyncpg"

    # computed fields
    sync_url: str = "None"
    async_url: str = "None"

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=CURRENT_FILE / "deployment/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def model_post_init(self, __context: dict) -> None:
        # automatically compute URLs after init
        self.sync_url = (
            f"{self.SYNC_DRIVER}://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.HOST}:{self.POSTGRES_EXPOSE_PORT}/{self.POSTGRES_DB}"
        )
        self.async_url = (
            f"{self.ASYNC_DRIVER}://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.HOST}:{self.POSTGRES_EXPOSE_PORT}/{self.POSTGRES_DB}"
        )


class MongoConfig(pydantic_settings.BaseSettings):
    MONGO_USER: str = None
    MONGO_PASSWORD: str = None
    MONGO_HOSTNAME: str = None
    MONGO_PORT: str = None
    MONGO_DB: str = None

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=CURRENT_FILE / "deployment/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


pg_config = PostgresConfig()
# mongo_config = MongoConfig()


# class Database(pydantic.BaseModel):
#     user: str | None = None  # Made optional for SQLite
#     password: str | None = None  # Made optional for SQLite
#     hostname: str | None = None  # Made optional for SQLite
#     port: int | None = None  # Made optional for SQLite
#     db_name: str
#     sync_driver: str
#     async_driver: str
#
#     @pydantic.computed_field
#     @property
#     def sync_conn_string(self) -> str:
#         """Generate a database connection string based on the driver."""
#         if self.sync_driver.startswith("sqlite"):
#             return f"{self.sync_driver}:///{self.db_name}"
#         else:
#             return (
#                 f"{self.sync_driver}://{self.user}:{self.password}@"
#                 f"{self.hostname}:{self.port}/{self.db_name}"
#             )
#
#     @pydantic.computed_field
#     @property
#     def async_conn_string(self) -> str:
#         """Generate a database connection string based on the driver."""
#         if self.async_driver.startswith("sqlite"):
#             return f"{self.async_driver}:///{self.db_name}"
#         else:
#             return (
#                 f"{self.async_driver}://{self.user}:{self.password}@"
#                 f"{self.hostname}:{self.port}/{self.db_name}"
#             )
#
#
# databases: dict[str, Database] = {
#     "sqlite": Database(
#         db_name="sqlite_db",
#         sync_driver="sqlite",
#         async_driver="sqlite+aiosqlite",
#     ),
#     "postgres": Database(
#         user=os.getenv("POSTGRES_USER") or "postgres",
#         password=os.getenv("POSTGRES_PASSWORD") or "postgres",
#         hostname=os.getenv("POSTGRES_HOSTNAME") or "localhost",
#         port=os.getenv("POSTGRES_PORT") or 5432,
#         db_name=os.getenv("POSTGRES_DB") or "LogsObsDb",
#         sync_driver="postgresql+psycopg2",
#         async_driver="postgresql+asyncpg",
#     ),
#     "mongo": Database(
#         user=os.getenv("MONGO_USER") or "mongo",
#         password=os.getenv("MONGO_PASSWORD") or "mongo",
#         hostname=os.getenv("MONGO_HOSTNAME") or "localhost",
#         port=os.getenv("MONGO_PORT") or 27017,
#         db_name=os.getenv("MONGO_DB") or "LogsPoC",
#         sync_driver="mongodb",  # no real use for sync in MongoDB client
#         async_driver="mongodb+motor",  # or just "mongodb" if using `motor`
#     ),
# }
