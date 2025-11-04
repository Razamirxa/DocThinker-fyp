from pydantic_settings import BaseSettings
from typing import List
import os

from pathlib import Path
from dotenv import load_dotenv

# Get the base directory (backend folder)
BASE_DIR = Path(__file__).resolve().parent

# Load .env file from the backend directory
env_path = BASE_DIR / '.env'
print(f"Looking for .env file at: {env_path}")
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    # Database settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fyp_db")
    
    # Construct database URL
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # RAG Engine settings
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DEFAULT_RAG_MODEL: str = os.getenv("DEFAULT_RAG_MODEL", "gemini-1.5-pro")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "semester-books")
    
    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env file

    print("Connecting with user:", POSTGRES_USER)
    print("Password:", POSTGRES_PASSWORD)
    print("Host:", POSTGRES_HOST)
    print("Port:", POSTGRES_PORT)
    print("Database:", POSTGRES_DB)

settings = Settings() 

