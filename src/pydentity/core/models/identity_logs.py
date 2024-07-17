from datetime import datetime, timezone
from beanie import Document, Link
from pydantic import Field

from pydentity.core.models.identity import Identity

class IdentityLog(Document):
    """
    Represents a log entry for actions performed by or on an Identity within the system.

    This class is designed to track various actions associated with identities, such as login attempts, password changes, and other significant events. Each log entry includes a reference to the identity, the action performed, a timestamp, and an optional dictionary for additional details.

    Attributes:
        identity (Link[Identity]): A reference link to the Identity object that the log entry is associated with. This allows for easy querying of all log entries related to a specific identity.
        action (str): A string describing the action that was performed. This should be a brief, descriptive phrase or keyword that can be used to categorize the log entry.
        timestamp (datetime): The timestamp when the action was logged. It defaults to the current UTC time when the log entry is created. This ensures that all log entries are time-stamped in a consistent timezone for accurate tracking and reporting.
        details (dict, optional): An optional dictionary that can hold additional information about the action. This can be used to store extra data that might be relevant for auditing or debugging purposes, such as IP addresses, device information, or specific changes made during the action.

    Class Settings:
        name (str): Specifies the collection name in MongoDB to be "identity_logs". This setting ensures that all log entries are stored in a dedicated collection, making them easier to manage and query.
    """
    identity: Link[Identity]
    action: str
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    details: dict = Field(default_factory=dict)

    class Settings:
        name = "identity_logs"