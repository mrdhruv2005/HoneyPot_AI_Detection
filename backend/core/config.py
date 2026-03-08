from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "Scam Intelligence Agent"
    DEBUG: bool = True
    
    # Database
    MONGO_URI: str = "mongodb://admin:password@localhost:27017"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Keys
    API_KEY_SECRET: str = "secret-key"  # For Evaluation Mode
    JWT_SECRET: str = "jwt-secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    
    # Callback
    CALLBACK_URL: str = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache()
def get_settings():
    return Settings()
