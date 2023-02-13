import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env="DATABASE_URL")
    # db_url: str = "postgresql://fastapi_traefik:fastapi_traefik@0.0.0.0:5432/fastapi_traefik"


settings = Settings()
