from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RABBITMQ_HOST: str = "localhost"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
