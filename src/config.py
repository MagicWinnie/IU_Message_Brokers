from pydantic import FilePath, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672

    WORDS_BLACKLIST_PATH: FilePath

    QUEUE1: str = "api2filter"
    QUEUE2: str = "filter2screaming"
    QUEUE3: str = "screaming2publish"

    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_EMAIL: EmailStr
    SMTP_PASSWORD: str
    EMAIL_RECEIVERS: list[EmailStr] = []

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
