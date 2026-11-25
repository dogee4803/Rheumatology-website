from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Rheumatology website"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/rheuma"
    SECRET_KEY: str = "dev-secret-change-in-prod"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()