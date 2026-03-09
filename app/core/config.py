from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Portfolio Backend API"

    # ======================
    # DATABASE
    # ======================
    MONGO_URL: str
    DATABASE_NAME: str = "portfolio_db"

    # ======================
    # JWT SETTINGS
    # ======================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ======================
    # GOOGLE DRIVE
    # ======================
    GOOGLE_DRIVE_FOLDER_ID: Optional[str] = None
    GOOGLE_CREDENTIALS_FILE: Optional[str] = None
    GOOGLE_CREDENTIALS_JSON: Optional[str] = None

    # ======================
    # CONFIG
    # ======================
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()