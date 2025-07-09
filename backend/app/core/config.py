from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, AnyHttpUrl
from typing import Any, List


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return self.DATABASE_URL

    class Config:
        env_file = ".env"
        extra = (
            "allow"  # or "ignore" instead of "forbid" if you're not using all env vars
        )


settings = Settings()
