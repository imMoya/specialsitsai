from pydantic_settings import BaseSettings
from pathlib import Path
from functools import lru_cache

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SpecialSitsAI API"
    BASE_PATH: str
    CORS_ORIGINS: list = ["*"]
    
    # Mail settings
    mail_host: str
    mail_username: str
    mail_password: str
    mail_port: str
    
    # Project settings
    data_dir: str
    project_path: str
    
    # API Keys
    openai_api_key: str
    langchain_api_key: str
    
    # Langchain settings
    langchain_tracing_v2: str
    
    # Substack credentials
    email_substack: str
    password_substack: str
    
    class Config:
        env_file = Path(__file__).parent.parent.parent / ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()