import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
PORT: int = int(os.getenv("PORT", "3000"))
MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_NAME: str = os.getenv("MONGODB_NAME", "streetballer")
JWT_SECRET: str = os.getenv("JWT_SECRET", "")
JWT_ACCESS_TTL: int = int(os.getenv("JWT_ACCESS_TTL", "3600"))
JWT_REFRESH_TTL: int = int(os.getenv("JWT_REFRESH_TTL", "2419200"))
