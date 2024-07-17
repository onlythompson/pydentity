from beanie import Document, Indexed, Link
from pydantic import Field
from typing import Optional
from pydentity.core.models.user import User

class UserProfile(Document):
    """
    Represents a user's profile in the database.

    This model is designed to store and manage user-specific information that extends beyond basic authentication details. It includes personal information, a biography, and user preferences.

    Attributes:
        user (Link[User]): A reference link to the User document. This creates a direct association between the UserProfile and its corresponding User document, ensuring that each profile is uniquely linked to a single user.
        first_name (Optional[str]): The user's first name. This field is optional and defaults to None.
        surname (Optional[str]): The user's surname or last name. This field is also optional and defaults to None.
        bio (Optional[str]): A short biography or personal statement about the user. This field is optional and can be used to share more about the user's interests, background, or anything they choose. Defaults to None.
        preferences (dict): A dictionary to store user-specific preferences. This can include settings related to the application's use, display options, or any other customizable user preferences. It uses a default factory to ensure it defaults to an empty dictionary if not explicitly set.

    Settings:
        name (str): Specifies the collection name in MongoDB to be "user_profiles". This setting directs where documents created from this model will be stored, organizing all user profile documents under the "user_profiles" collection.
    """
    user: Link[User]
    first_name: Optional[str] = None
    surname: Optional[str] = None
    bio: Optional[str] = None
    preferences: dict = Field(default_factory=dict)

    class Settings:
        name = "user_profiles"
