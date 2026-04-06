"""
core/config.py
Configuración centralizada usando pydantic-settings.
Lee variables desde .env (dev) o Vault (prod) — nunca hardcodeadas.
"""
from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from functools import lru_cache

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnv(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION  = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",           # ignora variables desconocidas (ej: GEMINI_API_KEY)
    )

    # ── App ──────────────────────────────────────────────────────────
    app_env: AppEnv = AppEnv.DEVELOPMENT
    log_level: str  = "INFO"

    # ── Base de datos ────────────────────────────────────────────────
    database_url: str = "sqlite+aiosqlite:///./data/pokemon.db"

    # ── Vector DB ────────────────────────────────────────────────────
    chromadb_path: Path        = Path("./data/vectors")
    chromadb_collection: str   = "pokemon_strategies"
    embedding_model: str       = "all-MiniLM-L6-v2"

    # ── APIs (SecretStr oculta el valor en logs) ─────────────────────
    gemini_api_key:     SecretStr | None = Field(default=None)
    pikalytics_api_key: SecretStr | None = Field(default=None)
    showdown_api_key:   SecretStr | None = Field(default=None)

    # ── Scraping ─────────────────────────────────────────────────────
    scraper_user_agent:         str   = "ShieldOps/1.0 (competitive research)"
    scraper_rate_limit_seconds: float = 2.0

    @field_validator("database_url")
    @classmethod
    def no_pickle_in_url(cls, v: str) -> str:
        """Previene DSNs inusuales que podrían apuntar a deserializadores."""
        forbidden = ("pickle://", "marshal://")
        if any(v.startswith(f) for f in forbidden):
            msg = "DSN de base de datos no permitido."
            raise ValueError(msg)
        return v

    @property
    def is_production(self) -> bool:
        return self.app_env == AppEnv.PRODUCTION


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton de configuración — importar y usar en toda la app."""
    return Settings()
