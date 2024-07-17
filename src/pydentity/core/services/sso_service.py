# src/pyidentity/core/services/sso_service.py

import jwt
from jwt.algorithms import RSAAlgorithm
import httpx
from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from typing import Optional, Dict
import time

from pydentity.models import User, SSOProvider, IdentityType
from pydentity.core.config import get_settings
from pydentity.utils.validators import validate_username

class SSOService:
    def __init__(self):
        self.settings = get_settings()
        self.http_client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.aclose()

    async def authenticate(self, provider: SSOProvider, token: str, authorization_code: Optional[str] = None) -> User:
        if provider == SSOProvider.google:
            return await self.authenticate_google(token)
        elif provider == SSOProvider.apple:
            return await self.authenticate_apple(token, authorization_code)
        elif provider == SSOProvider.facebook:
            return await self.authenticate_facebook(token)
        else:
            raise ValueError(f"Unsupported SSO provider: {provider}")

    async def authenticate_google(self, token: str) -> User:
        try:
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), self.settings.GOOGLE_CLIENT_ID)
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            google_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo.get('name')
            
            return await self._get_or_create_sso_user(SSOProvider.google, google_id, email, name)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid Google token: {str(e)}")

    async def authenticate_apple(self, identity_token: str, authorization_code: Optional[str] = None) -> User:
        try:
            # Fetch Apple's public key
            keys = await self._get_apple_public_keys()

            # Decode and verify the identity token
            decoded = await self._verify_apple_token(identity_token, keys)

            apple_user_id = decoded['sub']
            email = decoded.get('email')
            name = decoded.get('name')

            if not email and authorization_code:
                # Handle first-time sign-in with private email
                user_info = await self._exchange_apple_auth_code(authorization_code)
                email = user_info.get('email')
                name = user_info.get('name')

            if not email:
                raise ValueError("Unable to retrieve email from Apple")

            return await self._get_or_create_sso_user(SSOProvider.apple, apple_user_id, email, name)
        except jwt.PyJWTError as e:
            raise HTTPException(status_code=400, detail=f"Invalid Apple token: {str(e)}")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def authenticate_facebook(self, access_token: str) -> User:
        try:
            # Verify the access token with Facebook
            user_info = await self._verify_facebook_token(access_token)
            
            facebook_id = user_info['id']
            email = user_info.get('email')
            name = user_info.get('name')

            if not email:
                raise ValueError("Email not provided by Facebook")

            return await self._get_or_create_sso_user(SSOProvider.facebook, facebook_id, email, name)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid Facebook token: {str(e)}")

    async def _get_or_create_sso_user(self, provider: SSOProvider, sso_id: str, email: str, name: Optional[str] = None) -> User:
        user = await User.get_by_sso_id(provider, sso_id)
        if not user:
            user = await User.get_by_email(email)
            if user:
                # Link existing user to SSO provider
                user.sso_provider = provider
                user.sso_id = sso_id
            else:
                # Create new user
                username = await self._generate_unique_username(email, name)
                user = User(
                    username=username,
                    email=email,
                    identity_type=IdentityType.sso_user,
                    sso_provider=provider,
                    sso_id=sso_id,
                    email_verified=True,
                    full_name=name
                )
            await user.save()
        return user

    async def _generate_unique_username(self, email: str, name: Optional[str] = None) -> str:
        base_username = name.split()[0].lower() if name else email.split('@')[0]
        base_username = ''.join(c for c in base_username if c.isalnum() or c == '_')
        
        username = base_username
        suffix = 1
        while not validate_username(username) or await User.get_by_username(username):
            username = f"{base_username}{suffix}"
            suffix += 1
        
        return username

    async def _get_apple_public_keys(self) -> Dict:
        response = await self.http_client.get('https://appleid.apple.com/auth/keys')
        return response.json()['keys']

    async def _verify_apple_token(self, token: str, keys: Dict) -> Dict:
        header = jwt.get_unverified_header(token)
        key = next(key for key in keys if key['kid'] == header['kid'])
        public_key = RSAAlgorithm.from_jwk(key)

        return jwt.decode(
            token,
            public_key,
            audience=self.settings.APPLE_CLIENT_ID,
            algorithms=['RS256']
        )

    async def _exchange_apple_auth_code(self, authorization_code: str) -> dict:
        client_secret = self._generate_apple_client_secret()
        
        response = await self.http_client.post(
            'https://appleid.apple.com/auth/token',
            data={
                'client_id': self.settings.APPLE_CLIENT_ID,
                'client_secret': client_secret,
                'code': authorization_code,
                'grant_type': 'authorization_code'
            }
        )
        
        if response.status_code != 200:
            raise ValueError("Failed to exchange authorization code")
        
        token_data = response.json()
        id_token = token_data['id_token']
        
        # Decode the ID token to get user information
        decoded = jwt.decode(id_token, options={"verify_signature": False})
        return {
            'email': decoded.get('email'),
            'name': decoded.get('name'),
            'sub': decoded.get('sub')
        }

    def _generate_apple_client_secret(self) -> str:
        now = int(time.time())
        expiration_time = now + 15777000  # 6 months in seconds

        payload = {
            'iss': self.settings.APPLE_TEAM_ID,
            'iat': now,
            'exp': expiration_time,
            'aud': 'https://appleid.apple.com',
            'sub': self.settings.APPLE_CLIENT_ID
        }

        headers = {
            'kid': self.settings.APPLE_KEY_ID,
            'alg': 'ES256'
        }

        return jwt.encode(
            payload,
            self.settings.APPLE_PRIVATE_KEY,
            algorithm='ES256',
            headers=headers
        )

    async def _verify_facebook_token(self, access_token: str) -> Dict:
        response = await self.http_client.get(
            'https://graph.facebook.com/me',
            params={
                'fields': 'id,name,email',
                'access_token': access_token
            }
        )
        
        if response.status_code != 200:
            raise ValueError("Invalid Facebook access token")
        
        return response.json()