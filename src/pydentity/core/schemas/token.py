from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """
    Token model for access token representation.

    Attributes:
        access_token (str): The JWT access token string.
        token_type (str): The type of token, typically "bearer".
    """
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """
    Payload model for JWT token.

    Attributes:
        sub (Optional[str]): The subject of the token which usually contains the user identifier. Defaults to None.
        exp (Optional[int]): The expiration time of the token as a UNIX timestamp. Defaults to None.
    """
    sub: Optional[str] = None
    exp: Optional[int] = None

class TokenData(BaseModel):
    """
    Data model for user information encoded in the token.

    Attributes:
        username (str): The username of the user the token is issued for.
    """

    username: str

class SSOLogin(BaseModel):
    """ Model for Single Sign-On login request. """
    token: str