from beanie import Document, Indexed, Link
from pydantic import Field
from typing import Dict, List
from datetime import datetime, timezone
from enum import Enum
from .role import Role


class IdentityType(str, Enum):
    """
    Enum for Identity Types.

    Attributes:
        user (str): Represents a user identity type.
        agent (str): Represents an agent identity type.
        ssouser (str): Represents an SSO user identity type.
    """

    user = 'user'
    agent = 'agent'
    sso_user = 'sso_user'

class SSOProvider(str, Enum):
    """
    Enumeration of supported Single Sign-On (SSO) providers.

    This class defines a set of constants representing the SSO providers that the system can integrate with for authentication purposes.

    Attributes:
        google (str): Represents the Google SSO provider.
        facebook (str): Represents the Facebook SSO provider.
        github (str): Represents the GitHub SSO provider.
        apple (str): Represents the Apple SSO provider.
    """
    google = 'google'
    facebook = 'facebook'
    github = 'github'
    apple = 'apple'

class VerificationStatus(str, Enum):
    """
    Enumeration of possible verification statuses for an identity.

    This class defines the various states an identity's verification process can be in, from unverified to verified.

    Attributes:
        unverified (str): The initial state of an identity before any verification action has been taken.
        pending (str): Indicates that the verification process has been initiated but not yet completed.
        verified (str): Indicates that the identity has been successfully verified.
    """
    unverified = 'unverified'
    pending = 'pending'
    verified = 'verified'

class Identity(Document):
    """
    Represents a generic identity in the system, serving as a base model for user accounts or any entity requiring authentication and authorization.

    This class encapsulates common attributes and methods required for identity management, including username uniqueness, role-based access control, and claims-based permissions.

    Attributes:
        username (Indexed[str]): A unique username for the identity. Must be between 5 to 50 characters.
        identity_type (IdentityType): The type of identity (e.g., user, admin). This helps in differentiating between different kinds of identities within the system.
        roles (List[Link[Role]]): A list of roles associated with the identity. Roles are used for role-based access control.
        claims (Dict[str, List[str]]): A dictionary of claims associated with the identity. Claims are used for fine-grained access control.
        is_active (bool): Indicates whether the identity is active. Only active identities are allowed to authenticate.
        verification_status (VerificationStatus): The verification status of the identity. Useful for email verification or two-factor authentication statuses.
        created_at (datetime): The timestamp when the identity was created. Automatically set to the current UTC time upon creation.
        updated_at (datetime): The timestamp when the identity was last updated. Automatically set to the current UTC time upon update.

    Settings:
        name (str): Specifies the collection name in MongoDB to be "identities".
        use_state_management (bool): Indicates whether state management features should be used. This can be useful for tracking changes to the document state.

    Methods:
        verify_identity: An abstract method that should be implemented by subclasses to define how an identity is verified.
        initiate_verification: An abstract method that should be implemented by subclasses to define how the verification process is initiated.
        by_username: A class method to find an identity document by its username.
        has_permission: Checks if the identity has a specific permission, either through roles.
        has_claims: Checks if the identity has a specific claim
        add_claim: Adds a claim to the identity.
        remove_claim: Removes a claim from the identity.
    """
    username: Indexed(str, unique=True) = Field(..., min_length=5, max_length=50)
    identity_type: IdentityType
    roles: List[Link[Role]] = []
    claims: Dict[str, List[str]] = Field(default_factory=dict)
    is_active: bool = True
    verification_status: VerificationStatus = VerificationStatus.unverified
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "identities"
        use_state_management = True

    async def verify_identity(self) -> bool:
        """ Verify the identity."""
        raise NotImplementedError("Subclasses must implement this method")

    async def initiate_verification(self) -> bool:
        """ Initiate the verification process for the identity."""
        raise NotImplementedError("Subclasses must implement this method")

    @classmethod
    async def by_username(cls, username: str):
        """
        Class method to find an identity document by its username.

        Parameters:
            username (str): The username of the identity to find.

        Returns:
            The found identity document, or None if no document matches the provided username.
        """
        return await cls.find_one(cls.username == username)

    async def has_role_permission(self, permission: str) -> bool:
        """
        Checks if the identity has a specific permission.

        This method checks the identity's roles and claims to determine if it has the specified permission.

        Parameters:
            permission (str): The permission to check for.

        Returns:
            bool: True if the identity has the specified permission, False otherwise.
        """
        # Check role-based permissions
        for role in self.roles:
            if permission in role.permissions:
                return True
    
        return False
    
    async def has_claims(self, claim_type: str, claim_value: str = None) -> bool:
        """
        Checks if the identity has a specific claim.

        This method checks the identity's roles and claims to determine if it has the specified permission.

        Parameters:
           claim_type (str): The type of the claim to check for.
           claim_value (str): The value of the claim to check for.

        Returns:
            bool: True if the identity has the specified claim, False otherwise.
        """
        # Check claim-based permissions
        if claim_type in self.claims:
            if claim_value:
                return claim_value in self.claims[claim_type]
            return True
        return False

    async def add_claim(self, claim_type: str, claim_value: str):
        """
        Adds a claim to the identity.

        If the claim type does not exist, it is created. If the claim value is not already present for the claim type, it is added.

        Parameters:
            claim_type (str): The type of the claim to add.
            claim_value (str): The value of the claim to add.

        Returns:
            None
        """
        if claim_type not in self.claims:
            self.claims[claim_type] = []
        if claim_value not in self.claims[claim_type]:
            self.claims[claim_type].append(claim_value)
        await self.save()

    async def remove_claim(self, claim_type: str, claim_value: str):
        """
        Removes a claim from the identity.

        If the claim value exists for the specified claim type, it is removed. If removing the claim value leaves the claim type empty, the claim type is also removed.

        Parameters:
            claim_type (str): The type of the claim to remove.
            claim_value (str): The value of the claim to remove.

        Returns:
            None
        """
        if claim_type in self.claims and claim_value in self.claims[claim_type]:
            self.claims[claim_type].remove(claim_value)
            if not self.claims[claim_type]:
                del self.claims[claim_type]
            await self.save()