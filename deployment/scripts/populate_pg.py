import pathlib
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    HOST: str = "localhost"
    POSTGRES_PORT: int = None
    POSTGRES_DB: str = None
    POSTGRES_USER: str = None
    POSTGRES_PASSWORD: str = None

    model_config = pydantic_settings.SettingsConfigDict(
        env_file=pathlib.Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

if __name__ == "__main__":
    pg: pydantic_settings.BaseSettings = Settings()

    print("Postgres worker_settings loaded:")
    print(f"HOST: {pg.HOST}")
    print(f"PORT: {pg.POSTGRES_PORT}")
    print(f"DB: {pg.POSTGRES_DB}")
    print(f"USER: {pg.POSTGRES_USER}")
    print(f"PASSWORD: {pg.POSTGRES_PASSWORD}")

    # Example: connecting with psycopg2 (synchronous)
    import psycopg2

    with psycopg2.connect(
        dbname=pg.POSTGRES_DB,
        user=pg.POSTGRES_USER,
        password=pg.POSTGRES_PASSWORD,
        host=pg.HOST,
        port=pg.POSTGRES_PORT,
    ) as conn:
        # Use context manager for cursor
        with conn.cursor() as cur:
            # Create table if not exists
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    value INT NOT NULL
                )
                """
            )

            # Insert example data
            for i in range(100):
                cur.execute(
                    "INSERT INTO test_table (name, value) VALUES (%s, %s)",
                    (f"example_{i}", i),
                )

            # Query and print results
            cur.execute("SELECT * FROM test_table")
            rows = cur.fetchall()
            for row in rows:
                print(row)

