from pydantic import FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RABBITMQ_HOST: str = "localhost"
    WORDS_BLACKLIST_PATH: FilePath

    QUEUE1: str = "api2filter"
    QUEUE2: str = "filter2screaming"
    QUEUE3: str = "screaming2publish"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
