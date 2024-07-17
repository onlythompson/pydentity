from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from pydentity.core.schemas.identity import IdentityBase
from pydentity.core.schemas.roles import RoleInDB


class AgentBase(IdentityBase):
    """
    Base model for an agent, extending the IdentityBase model with an API key.

    Attributes:
        api_key (str): The API key assigned to the agent for authentication. It must be between 32 to 64 characters long.
    """
    api_key: str = Field(..., min_length=32, max_length=64)

class AgentCreate(AgentBase):
    """
    Model for creating a new agent.

    Inherits all attributes from AgentBase without adding additional fields. Used specifically for creating new agent instances.
    """
    pass

class AgentUpdate(BaseModel):
    """
    Model for updating an existing agent's information.

    Allows for the optional update of the agent's API key and active status.

    Attributes:
        api_key (Optional[str]): The new API key for the agent. It must be between 32 to 64 characters long if provided.
        is_active (Optional[bool]): The new active status of the agent. True for active, False for inactive.
    """
    api_key: Optional[str] = Field(None, min_length=32, max_length=64)
    is_active: Optional[bool] = None

class AgentInDB(AgentBase):
    """
    Database model for an agent, extending AgentBase with database-specific fields.

    Attributes:
        id (str): The unique identifier for the agent.
        roles (List[RoleInDB]): A list of roles assigned to the agent.
        claims (Dict[str, List[str]]): A dictionary of claims associated with the agent.
        created_at (datetime): The timestamp when the agent was created.
        updated_at (datetime): The timestamp when the agent was last updated.
        last_active (Optional[datetime]): The timestamp when the agent was last active. None if never active.
        verification_code (Optional[str]): An optional verification code for the agent. None if not applicable.

    Class Config:
        orm_mode (bool): Enables ORM mode for compatibility with ORMs like SQLAlchemy. This allows for the use of Pydantic models with ORMs directly.
    """
    id: str
    roles: List[RoleInDB] = []
    claims: Dict[str, List[str]] = {}
    created_at: datetime
    updated_at: datetime
    last_active: Optional[datetime] = None
    verification_code: Optional[str] = None

    class Config:
        orm_mode = True

class AgentOut(AgentBase):
    """
    Output model for an agent, extending AgentBase with output-specific fields.

    Attributes:
        id (str): The unique identifier for the agent.
        roles (List[RoleInDB]): A list of roles assigned to the agent, for output purposes.
        created_at (datetime): The timestamp when the agent was created, for output purposes.

    Class Config:
        orm_mode (bool): Enables ORM mode for compatibility with ORMs like SQLAlchemy, similar to AgentInDB.
    """
    id: str
    roles: List[RoleInDB] = []
    created_at: datetime

    class Config:
        orm_mode = True
