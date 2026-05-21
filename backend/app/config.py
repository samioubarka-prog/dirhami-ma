from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Dirhami"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://dirhami_user:password@localhost:5432/dirhami_db"

    # JWT
    SECRET_KEY: str = "votre-cle-secrete-changez-cela-en-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    FRONTEND_URL: str = "http://localhost:5500"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
