"""
FastAPI application configuration and settings.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Porticus Signis Idearum Personatis"
    DEBUG: bool = True
    PORT: int = 4200
    
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "student"
    DB_PASSWORD: str = "student_secure_password"
    DB_NAME: str = "wp_labs"
    
    # JWT settings
    JWT_ACCESS_SECRET: str = "your-access-secret-key-change-in-production"
    JWT_REFRESH_SECRET: str = "your-refresh-secret-key-change-in-production"
    JWT_ACCESS_EXPIRATION: int = 15  # minutes
    JWT_REFRESH_EXPIRATION: int = 10080  # minutes (7 days)
    
    # OAuth settings
    YANDEX_CLIENT_ID: str = ""
    YANDEX_CLIENT_SECRET: str = ""
    YANDEX_REDIRECT_URI: str = "http://localhost:4200/api/auth/oauth/yandex/callback"
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
