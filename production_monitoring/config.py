"""Environment-backed configuration for the monitored auth service."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Load authentication and monitoring settings from the environment."""

    jwt_secret_key: str
    sentry_dsn: str
    environment: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
