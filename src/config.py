from pydantic import FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RABBITMQ_HOST: str = "localhost"
    WORDS_BLACKLIST_PATH: FilePath

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
