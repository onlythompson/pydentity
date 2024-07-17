from beanie import Document, Indexed
from typing import List, Optional


class Role(Document):
    """
    Role document model for role-based access control.

    Inherits from beanie.Document to leverage MongoDB document mapping.

    Attributes:
        name (Indexed[str]): The unique name of the role. This field is indexed to ensure uniqueness.
        description (Optional[str]): An optional description of the role. Defaults to None.
        permissions (List[str]): A list of permissions associated with the role. Defaults to an empty list.

    Settings:
        name (str): Specifies the collection name in MongoDB to be "roles".
    """
    name: Indexed(str, unique=True)
    description: Optional[str] = None
    permissions: List[str] = []

    class Settings:
        name = "roles"