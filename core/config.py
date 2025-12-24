from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field
from pathlib import Path

class Settings(BaseSettings):
    # DB
    PROD_DB_NAME: str = ""
    PROD_DB_USER: str = ""
    PROD_DB_PASSWORD: str = ""
    PROD_DB_HOST: str = ""
    PROD_DB_PORT: str = ""

    # TG
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_BOT_SECRET_TOKEN: str = ""

    @computed_field
    @property
    def database_url(self) -> str:
            return f"postgresql+asyncpg://{self.PROD_DB_USER}:{self.PROD_DB_PASSWORD}@{self.PROD_DB_HOST}:{self.PROD_DB_PORT}/{self.PROD_DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore")


_settings: Settings | None = None

def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings