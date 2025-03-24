from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./project.db"
    LOGGER_MODE: str = "console"
    TELEGRAM_API_KEY: str
    TELEGRAM_ADMIN_ID: str
    JWT_SECRET: str
    API_SERVERS: list[str]
    YOOMONEY_TOKEN: str
    YOOMONEY_RECEIVER: str
    ADMIN_SECRET: str
    model_config = ConfigDict(extra="ignore", env_file=".env")


settings = Settings()




print(settings.DATABASE_URL)