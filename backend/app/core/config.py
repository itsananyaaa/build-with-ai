import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load variables from .env file into os environment
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "PersonaAI Backend"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secret_key_change_me")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Vector DB
    CHROMA_DB_DIR: str = "./chroma_db"
    
    # LLM
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Redis Queue
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
