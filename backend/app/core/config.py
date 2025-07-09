import os
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, AnyHttpUrl
from typing import Any, List


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"

    # API Configuration
    API_V1_STR: str = "/api/v1"

    # CORS Origins - more flexible for different environments
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Database - make optional for testing
    DATABASE_URL: str | None = None

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_LEVEL: str = "INFO"

    # Database initialization settings
    FIRST_SUPERUSER: str = "admin@yourdomain.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis"

    # Testing specific
    TEST_DATABASE_URL: str | None = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.ENVIRONMENT == "testing":
            return "sqlite:///./test.db"
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is required for non-testing environments")
        return self.DATABASE_URL

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "testing"

    class Config:
        env_file = ".env"
        extra = "allow"


# Load environment-specific settings
def get_settings() -> Settings:
    env = os.getenv("ENVIRONMENT", "development")
    env_file = f".env.{env}"

    # Fallback to .env if specific env file doesn't exist
    if not os.path.exists(env_file):
        env_file = ".env"

    return Settings(_env_file=env_file)


settings = get_settings()
