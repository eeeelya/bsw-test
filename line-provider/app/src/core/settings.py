from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    API_PREFIX: str = "/api/v1"

    LINE_PROVIDER_NAME: str = "line-provider"
    BET_MAKER_NAME: str = "bet-maker"

    # PostgreSQL
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"

    # Kafka
    KAFKA_NODES: str = "kafka:9092"

    @property
    def DB_URL(self) -> str:
        _format: str = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"

        return _format.format(
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            name=self.DB_NAME,
        )


env_settings: EnvSettings = EnvSettings()
