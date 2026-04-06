from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "GrowthOperator Worker"
    
    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6381/0"
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5434/growthoperator"

    # LLM
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
