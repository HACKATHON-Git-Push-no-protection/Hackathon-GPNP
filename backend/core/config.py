# core/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    POSTGRES_URL: str = "postgresql+asyncpg://admin:password@postgres:5432/sep4db"

    class Config:
        env_file = ".env"

settings = Settings()
