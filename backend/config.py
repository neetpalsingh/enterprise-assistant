from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    ollama_base_url: str = "http://localhost:11434"
    database_url: str = "sqlite:///./enterprise_assistant.db"
    default_llm: str = "openai"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
