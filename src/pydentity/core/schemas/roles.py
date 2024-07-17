"""Role schemas."""
from typing import List, Optional
from pydantic import BaseModel

class RoleBase(BaseModel):
    """
    Base model for a role, defining the core attributes shared by all role models.

    Attributes:
        name (str): The name of the role. This should be unique across all roles.
        description (Optional[str]): An optional description of the role, providing more context about its purpose and usage.
    """
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    """
    Model for creating a new role, extending RoleBase with permissions.

    This model is used when a new role is being created, allowing the specification of permissions associated with the role.

    Attributes:
        permissions (List[str]): A list of permissions to be associated with the role upon creation. Defaults to an empty list if no permissions are specified.
    """
    permissions: List[str] = []

class RoleUpdate(RoleBase):
    """
    Model for updating an existing role, extending RoleBase with optional permissions.

    This model allows for the updating of a role's name, description, and permissions. Permissions can be optionally updated, allowing for flexibility in role management.

    Attributes:
        permissions (Optional[List[str]]): An optional list of permissions for the role. If provided, it updates the role's permissions; otherwise, the role's permissions remain unchanged.
    """
    permissions: Optional[List[str]] = None

class RoleInDB(RoleBase):
    """
    Database model for a role, extending RoleBase with database-specific fields.

    This model represents how a role is stored in the database, including its unique identifier and permissions.

    Attributes:
        id (str): The unique identifier for the role.
        permissions (List[str]): A list of permissions associated with the role. This list is stored in the database along with the role.

    Class Config:
        orm_mode (bool): Enables ORM mode for compatibility with ORMs like SQLAlchemy. This allows for the use of Pydantic models with ORMs directly, facilitating the interaction between the database and the application.
    """
    id: str
    permissions: List[str] = []

    class Config:
        orm_mode = True