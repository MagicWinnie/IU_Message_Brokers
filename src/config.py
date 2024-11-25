from pydantic import FilePath, EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RABBITMQ_HOST: str = "localhost"
    WORDS_BLACKLIST_PATH: FilePath

    QUEUE1: str = "api2filter"
    QUEUE2: str = "filter2screaming"
    QUEUE3: str = "screaming2publish"

    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: SecretStr
    EMAIL_RECEIVERS: list[EmailStr] = []

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
