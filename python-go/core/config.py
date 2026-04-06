"""
core/config.py — Configuración ShieldOps GO
"""
from __future__ import annotations
from pathlib import Path
from functools import lru_cache
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    app_env:            str        = "development"
    log_level:          str        = "INFO"
    gemini_api_key:     SecretStr | None = Field(default=None)
    database_url:       str        = "sqlite+aiosqlite:///./data/go.db"
    chromadb_path:      Path       = Path("./data/vectors_go")
    scraper_rate_limit_seconds: float = 2.0

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
