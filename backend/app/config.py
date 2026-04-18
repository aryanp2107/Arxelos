"""
Application settings — loaded from environment variables / .env file.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration for the Arxelos platform."""

    # --- App ---
    APP_NAME: str = "Arxelos"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # --- Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --- CORS ---
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://arxelos.com",
    ]

    # --- Model paths (populated as models are added) ---
    TUMOR_MODEL_PATH: str = "models/tumor_classifier.h5"
    # LESIONS_MODEL_PATH: str = ""
    # RAG_INDEX_PATH: str = ""

    # --- External APIs (for Model 3 RAG) ---
    OPENAI_API_KEY: str = ""
    # CHROMA_PERSIST_DIR: str = "data/chroma_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
