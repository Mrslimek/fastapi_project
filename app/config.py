from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PG_USER: str
    PG_PASSWORD: str
    PG_NAME: str
    PG_HOST: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        # TODO: Разобрать, почему .env не подтягивается из корня
        # и приходится использовать pathlib
        env_file = Path(__file__).parent.parent / ".env"


settings = Settings()
