from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PG_USER: str
    PG_PASSWORD: str
    PG_NAME: str
    PG_HOST: str

    class Config:
        env_file = Path(__file__).parent.parent / ".env"


settings = Settings()
