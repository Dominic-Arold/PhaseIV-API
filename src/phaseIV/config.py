from pathlib import Path
from datetime import timedelta

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration for the PhaseIV client and API server.
    All fields can be overridden via environment variables (case-insensitive).
    """

    model_config = SettingsConfigDict(
        env_prefix="PHASEIV_",        # all env vars are PHASEIV_*
        env_file=".env",              # optional .env file support
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    cache_dir: Path = Path.home() / ".cache" / "phaseIV"
    cache_enabled: bool = True
    cache_ttl_hours: float = 24.0
    http_timeout: float = 10.0

    @field_validator("cache_dir", mode="before")
    @classmethod
    def expand_path(cls, v: object) -> Path:
        return Path(v).expanduser().resolve()

    @property
    def cache_ttl(self) -> timedelta:
        return timedelta(hours=self.cache_ttl_hours)


# Module-level singleton — import this everywhere
settings = Settings()
