"""Environment-backed configuration for the authentication service."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Load the shared JWT signing secret from the environment."""

    jwt_secret_key: str

    model_config = SettingsConfigDict(env_file=".env")
