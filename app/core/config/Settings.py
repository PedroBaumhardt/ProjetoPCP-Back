from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

from typing import cast

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    _instance: ClassVar["Settings | None"] = None

    DATABASE_USER:     str
    DATABASE_PASSWORD: str
    DATABASE_HOST:     str
    DATABASE_PORT:     int
    DATABASE_NAME:     str

    SQLALCHEMY_DEBUG:  bool = False

    def get_database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            database=self.DATABASE_NAME,
        )

    @classmethod
    def get_instance(cls) -> "Settings":
        if cls._instance is None:
            cls._instance = cls()
        return cast("Settings", cls._instance)