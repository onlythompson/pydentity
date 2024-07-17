from pydantic import BaseModel, Field
from typing import Optional

class PyIdentityConfig(BaseModel):
    secret_key: str = Field(..., min_length=32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    mongodb_url: Optional[str] = None
    mongodb_db_name: str = "pydentity"
    allow_user_registration: bool = True
    require_email_verification: bool = False
    password_reset_token_expire_hours: int = 24