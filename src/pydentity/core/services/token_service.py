
# src/pyidentity/core/services/token_service.py

from jose import JWTError, jwt
from datetime import datetime, timedelta
from pyidentity.core.config import get_settings

class TokenService:
    def __init__(self):
        self.settings = get_settings()

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str):
        return jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM])
