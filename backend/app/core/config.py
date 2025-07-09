from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, AnyHttpUrl
from typing import Any, List


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database initialization settings
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return self.DATABASE_URL

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
