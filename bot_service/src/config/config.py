from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    """Настройки приложения."""

    # Telegram
    TELEGRAM_BOT_TOKEN: str = Field(env="TELEGRAM_BOT_TOKEN")

    # Django API
    DJANGO_API_URL: str = Field(env="DJANGO_API_URL")
    DJANGO_API_TIMEOUT: int = Field(env="DJANGO_API_TIMEOUT")

    # Redis для кэширования
    REDIS_HOST: str = Field("todo_redis", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    REDIS_DB: int = Field(0, env="REDIS_DB")

    # Настройки приложения
    DEBUG: bool = Field(False, env="DEBUG")

    # JWT
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def api_base_url(self) -> str:
        return self.DJANGO_API_URL.rstrip("/")


settings = Settings()
