import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
    SECRET_KEY = str(os.getenv("SECRET_KEY"))
    ALGORITHM = os.getenv("ALGORITHM", "")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", ""))
    
    if not DATABASE_URL or not SECRET_KEY or not ALGORITHM:
        raise ValueError("environment variables are required!")
        
settings = Settings()
