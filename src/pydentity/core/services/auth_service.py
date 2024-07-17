"""Authentication service module."""
from datetime import datetime, timezone
import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydentity.core.models import User, Agent, Identity
from pydentity.core.models.identity import SSOProvider
from pydentity.core.services.token_service import TokenService
from pydentity.core.config import get_settings
from passlib.context import CryptContext


logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, token_service: TokenService = Depends()):
        self.token_service = token_service
        self.settings = get_settings()

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str):
        user = await User.find_one(User.username == username)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def authenticate_agent(self, api_key: str):
        agent = await Agent.find_one(Agent.api_key == api_key)
        return agent

    async def get_current_identity(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = self.token_service.decode_token(token)
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        identity = await Identity.find_one(Identity.username == username)
        if identity is None:
            raise credentials_exception
        return identity

    """ Single Sign-On (SSO) Service """
    async def authenticate_sso(self, provider: SSOProvider, token: str, authorization_code: Optional[str] = None) -> User:
        """
        Authenticate a user using SSO provider.

        Args:
            provider (SSOProvider): The SSO provider (e.g., Google, Apple, Facebook).
            token (str): The authentication token from the SSO provider.
            authorization_code (Optional[str]): The authorization code, required for some providers (e.g., Apple).

        Returns:
            User: The authenticated user object.

        Raises:
            HTTPException: If authentication fails or the SSO provider is not supported.
        """
        try:
            if provider == SSOProvider.google:
                user = await self.sso_service.authenticate_google(token)
            elif provider == SSOProvider.apple:
                user = await self.sso_service.authenticate_apple(token, authorization_code)
            elif provider == SSOProvider.facebook:
                user = await self.sso_service.authenticate_facebook(token)
            #To be implemented
            # elif provider == SSOProvider.github:
            #     user = await self.sso_service.authenticate_github(token)
            else:
                raise ValueError(f"Unsupported SSO provider: {provider}")

            if not user:
                raise ValueError(f"Authentication failed for provider: {provider}")

            # Additional post-authentication actions
            await self._post_authentication_actions(user, provider)

            return user

        except ValueError as e:
            logger.error(f"SSO Authentication error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.exception(f"Unexpected error during SSO authentication: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred during authentication")

    async def _post_authentication_actions(self, user: User, provider: SSOProvider):
        """
        Perform actions after successful authentication.

        Args:
            user (User): The authenticated user.
            provider (SSOProvider): The SSO provider used for authentication.
        """
        # Update last login timestamp
        user.last_login = datetime.now(timezone.utc)
        
        # Check if email verification is required
        if self.settings.REQUIRE_EMAIL_VERIFICATION and not user.email_verified:
            user.email_verified = True  # SSO providers typically verify emails
        
        # Log the successful authentication
        logger.info(f"User {user.username} authenticated via {provider}")
        
        # You might want to create or update a login history entry here
        
        await user.save()
