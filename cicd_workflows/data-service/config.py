"""Environment-backed configuration for the protected data service."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Load the shared JWT secret used by the service cluster."""

    jwt_secret_key: str

    model_config = SettingsConfigDict(env_file=".env")
