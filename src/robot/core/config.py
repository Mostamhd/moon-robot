import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str | None = None

    # Robot initialization
    START_POSITION: str = os.getenv("START_POSITION", "(0, 0)")
    START_DIRECTION: str = os.getenv("START_DIRECTION", "NORTH")

    # Internal properties
    @property
    def start_position(self) -> tuple:
        return eval(self.START_POSITION)

    @property
    def start_direction(self) -> str:
        return self.START_DIRECTION

    @property
    def database_url(self) -> str:
        """Return the database URL based on environment"""
        # Check if we're in a Docker container
        in_docker = (
            Path("/.dockerenv").exists() or os.getenv("DOCKER_ENV", "false") == "true"
        )

        if in_docker:
            return "postgresql+asyncpg://robotuser:robotpass@db:5432/moonrobot"
        return os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://robotuser:robotpass@localhost:5432/moonrobot",
        )


settings = Settings()
