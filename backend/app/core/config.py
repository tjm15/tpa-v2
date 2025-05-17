# app/core/config.py
import os
from typing import List, Union, Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv() # Load .env file if present

class Settings(BaseSettings):
    PROJECT_NAME: str = "TPA v2 Backend"
    API_V1_STR: str = "/api/v1"

    # CORS Origins
    BACKEND_CORS_ORIGINS: List[str] = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

    # Database (Example for PostgreSQL, adjust as needed)
    # POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    # POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    # POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    # POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tpa_v2_db")
    # DATABASE_URL: Optional[str] = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db") # Default to SQLite for easy start

    # Example for JWT token
    # SECRET_KEY: str = os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_changed")
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # 30 minutes

    class Config:
        case_sensitive = True
        # If you have a .env file, pydantic-settings will load it.
        # env_file = ".env" 


settings = Settings()
