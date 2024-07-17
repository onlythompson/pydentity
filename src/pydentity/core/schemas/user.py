from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List, Optional
from datetime import datetime

from pydentity.core.models.identity import SSOProvider
from pydentity.core.schemas.roles import RoleInDB
from .identity import UserIdentity

class UserBase(UserIdentity):
    """
    Base model for user information.

    Inherits from UserIdentity to include identity-specific attributes.

    Attributes:
        email (EmailStr): The email address of the user. Must be a valid email format.
        is_active (bool): Flag indicating if the user account is active. Defaults to True.
    """

    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    """
    Model for creating a new user.

    Inherits from UserBase and adds a password field.

    Attributes:
        password (str): The password for the new user account. Must be at least 8 characters long.
    """

    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """
    Model for updating user information.

    Allows for optional updates to username, email, and is_active status.

    Attributes:
        username (Optional[str]): The new username for the user. Must be between 5 to 50 characters if provided.
        email (Optional[EmailStr]): The new email address for the user. Must be a valid email format if provided.
        is_active (Optional[bool]): Flag indicating if the user account should be active or not.
    """
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    """
    Database model for user information.

    Inherits from UserBase and includes database-specific fields such as user ID, hashed password, and timestamps.

    Attributes:
        id (str): The unique identifier for the user.
        hashed_password (str): The hashed password for the user.
        created_at (datetime): The timestamp when the user account was created.
        updated_at (datetime): The timestamp when the user account was last updated.

    Config:
        from_attributes (bool): Indicates that ORM mode should be enabled, allowing for ORM objects to be used.
    """

    id: str
    hashed_password: str
    roles: List[RoleInDB] = []
    claims: Dict[str, List[str]] = {}
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    email_verified: bool = False
    sso_provider: Optional[SSOProvider] = None
    sso_id: Optional[str] = None

    class Config:
        orm_mode = True

class UserOut(UserBase):
    """
    Model for outputting user information.

    Inherits from UserBase and includes fields for user ID and account creation timestamp.

    Attributes:
        id (str): The unique identifier for the user.
        created_at (datetime): The timestamp when the user account was created.

    Config:
        from_attributes (bool): Indicates that ORM mode should be enabled, allowing for ORM objects to be used.
    """

    id: str
    roles: List[RoleInDB] = []
    claims: Dict[str, List[str]] = {}
    created_at: datetime
    email_verified: bool

    class Config:
        orm_mode = True