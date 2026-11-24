from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "SmartCampus AI API"
    app_description: str = "Backend API for SmartCampus AI"
    app_version: str = "1.0.0"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://smartcampus:smartcampus_dev_password@localhost:5432/smartcampus"
    session_ttl_hours: int = 24
    max_messages_per_session: int = 50
    max_message_length: int = 1000
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
        ]
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return [str(origin).strip() for origin in value if str(origin).strip()]
        return []


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()