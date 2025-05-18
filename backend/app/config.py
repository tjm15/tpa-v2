from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Core DB
    database_url: str = "postgresql://tpa:tpa@db:5432/tpa"  # Default for development, can be overridden by .env
    database_user: str = "tpa"
    database_password: str = "tpa"
    database_host: str = "db"
    database_port: int = 5432
    database_name: str = "tpa"

    # AI / Graph / Vector
    vector_dim: int = 768
    graph_name: str = "default_graph"

    # FastAPI runtime
    environment: str = "development"
    api_port: int = 8000
    api_host: str = "0.0.0.0"
    log_level: str = "debug"
    reload: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"  # Allow extra env vars in .env

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
