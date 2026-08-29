"""
LifeOps API — Configuration
============================
Centralized settings using Pydantic Settings.
Reads from .env file automatically.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    supabase_jwt_secret: str = ""
    supabase_schema: str = "lifeops"

    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # CORS
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000,http://localhost:1313,http://127.0.0.1:1313,https://datalaria.com,https://www.datalaria.com,https://datalaria-app-lifeops.netlify.app"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.
    Uses lru_cache so the .env file is only read once.
    """
    return Settings()
