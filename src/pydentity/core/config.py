# src/pyidentity/core/config.py

from pydantic import BaseSettings, EmailStr, field_validator
from typing import Optional, List, Union
from functools import lru_cache

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Pydentity"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # Security Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database Settings
    MONGODB_URL: str
    MONGODB_DB_NAME: str = "pydentity"

     # SSO Settings
    GOOGLE_CLIENT_ID: str
    APPLE_CLIENT_ID: str
    APPLE_TEAM_ID: str
    APPLE_KEY_ID: str
    APPLE_PRIVATE_KEY: str
    FACEBOOK_APP_ID: str
    FACEBOOK_APP_SECRET: str

    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8080", "https://localhost", "https://localhost:8080"]

    # Email Settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # Admin User
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    # Authentication Settings
    USERS_OPEN_REGISTRATION: bool = False
    EMAIL_VERIFICATION_REQUIRED: bool = True

    # Password Settings
    MIN_PASSWORD_LENGTH: int = 8
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    @field_validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Ensure BACKEND_CORS_ORIGINS is a list of strings"""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        #raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()