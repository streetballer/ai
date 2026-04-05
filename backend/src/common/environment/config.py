import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
PORT: int = int(os.getenv("PORT", "3000"))
FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:4000")
MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_NAME: str = os.getenv("MONGODB_NAME", "streetballer")
JWT_SECRET: str = os.getenv("JWT_SECRET", "")
JWT_ACCESS_TTL: int = int(os.getenv("JWT_ACCESS_TTL", "3600"))
JWT_REFRESH_TTL: int = int(os.getenv("JWT_REFRESH_TTL", "2419200"))
PASSWORD_RESET_TOKEN_TTL: int = int(os.getenv("PASSWORD_RESET_TOKEN_TTL", "3600"))
EMAIL_VERIFICATION_TOKEN_TTL: int = int(os.getenv("EMAIL_VERIFICATION_TOKEN_TTL", "86400"))
SMTP_HOST: str = os.getenv("SMTP_HOST", "")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER: str = os.getenv("SMTP_USER", "")
SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM: str = os.getenv("SMTP_FROM", "")
