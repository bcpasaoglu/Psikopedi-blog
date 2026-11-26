"""Application settings loaded from environment variables (and an optional .env file)."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    database_url: str = f"sqlite:///{BASE_DIR / 'psikopedi.db'}"
    cors_origins: str = ""

    # Admin authentication. Login is disabled until all three are set (fail closed).
    admin_username: str = ""
    admin_password_hash: str = ""  # bcrypt hash, see `python -m backend.hash_password`
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    seed_sample_data: bool = True

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def auth_configured(self) -> bool:
        return bool(self.admin_username and self.admin_password_hash and self.jwt_secret)


@lru_cache
def get_settings() -> Settings:
    return Settings()
