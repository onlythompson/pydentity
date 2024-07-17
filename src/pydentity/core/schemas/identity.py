from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime




class IdentityBase(BaseModel):
    """
    Base model for identity.

    Attributes:
        username (str): The username of the identity. Must be between 5 to 50 characters.
        IdentityType (IdentityType): The type of identity, either user or agent.
        is_active (bool): Flag indicating if the identity is active. Defaults to True.
    """

    username: str = Field(..., min_length=5, max_length=50)
    IdentityType: IdentityType
    is_active: bool = True

class UserIndentity(IdentityBase):
    """
    User identity model.

    Inherits from IdentityBase with IdentityType set to user.
    """

    IdentityType = IdentityType.user

class AgentIdentity(IdentityBase):
    """
    Agent identity model.

    Inherits from IdentityBase with IdentityType set to agent.
    """
    IdentityType = IdentityType.agent

