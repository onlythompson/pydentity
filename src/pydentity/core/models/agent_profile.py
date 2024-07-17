from beanie import Document, Indexed, Link
from pydantic import Field
from typing import List, Optional

from pydentity.core.models.agent import Agent


class AgentProfile(Document):
    """
    Represents an agent's profile in the database.

    This model is used to store and manage information related to an agent's profile, including their capabilities, description, and additional metadata.

    Attributes:
        agent (Link[Agent]): A link to the Agent document this profile belongs to. This creates a reference in the database to the Agent document.
        description (Optional[str]): An optional description of the agent's profile. Provides additional information about the agent. Defaults to None.
        capabilities (List[str]): A list of strings representing the capabilities or skills of the agent. This can include anything from languages spoken to technical skills. Defaults to an empty list.
        metadata (dict): A dictionary for storing additional metadata about the agent. This can be used to store any extra information that doesn't fit into the other fields. Defaults to an empty dictionary.

    Settings:
        name (str): Specifies the collection name in MongoDB to be "agent_profiles". This is where the documents created from this model will be stored.
    """
    agent: Link[Agent]
    description: Optional[str] = None
    capabilities: List[str] = []
    metadata: dict = Field(default_factory=dict)

    class Settings:
        name = "agent_profiles"