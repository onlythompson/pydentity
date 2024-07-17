from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

from pydentity.core.models.identity import SSOProvider


class Token(BaseModel):
    """
    Represents an authentication token.

    Attributes:
        access_token (str): The token that can be used to authenticate a user in subsequent requests.
        token_type (str): The type of the token, typically "bearer".
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Represents the data encoded in an authentication token.

    Attributes:
        username (Optional[str]): The username of the user the token represents. Can be None if the token does not include user information.
    """
    username: Optional[str] = None

class SSOLogin(BaseModel):
    """
    Represents a request for logging in using Single Sign-On (SSO).

    Attributes:
        provider (SSOProvider): The SSO provider through which the login is attempted.
        token (str): The token provided by the SSO service to authenticate the user.
        authorization_code (Optional[str]): An optional authorization code that might be required by some SSO providers.
    """
    provider: SSOProvider
    token: str
    authorization_code: Optional[str] = None

class ClaimUpdate(BaseModel):
    """
    Represents a request to update a user's claim.

    Attributes:
        claim_type (str): The type of the claim to be updated.
        claim_value (str): The new value for the claim.
    """
    claim_type: str
    claim_value: str

class PasswordReset(BaseModel):
    """
    Represents a request to reset a user's password.

    Attributes:
        email (EmailStr): The email address of the user requesting a password reset.
    """
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """
    Represents a request to confirm a password reset.

    Attributes:
        token (str): The token provided to the user for password reset confirmation.
        new_password (str): The new password chosen by the user. Must be at least 8 characters long.
    """
    token: str
    new_password: str = Field(..., min_length=8)

class EmailVerification(BaseModel):
    """
    Represents a request to verify an email address.

    Attributes:
        token (str): The token provided to the user for email verification.
    """
    token: str

class IdentityVerificationInitiate(BaseModel):
    """
    Represents a request to initiate identity verification.

    Attributes:
        identity_id (str): The unique identifier of the identity to be verified.
    """
    identity_id: str

class IdentityVerificationComplete(BaseModel):
    """
    Represents a request to complete identity verification.

    Attributes:
        identity_id (str): The unique identifier of the identity being verified.
        verification_code (str): The verification code that was sent to the identity for verification purposes.
    """
    identity_id: str
    verification_code: str
