from beanie import Indexed
from pydantic import EmailStr, Field
from typing import Optional
from datetime import datetime

from pydentity.core.models.identity import SSOProvider, VerificationStatus


class User(Identity):
        """
    Represents a user in the system, extending the Identity model.

    This class adds specific attributes related to a user's account, such as email, password, verification status, and last login information. It also provides a class method to find a user by email.

    Attributes:
        email (Indexed[EmailStr]): The user's email address. It is indexed and unique, ensuring no two users can share the same email.
        hashed_password (str): The user's password in a securely hashed format. This ensures that plain text passwords are never stored in the database.
        # is_verified (bool): A flag indicating whether the user's email address has been verified. Defaults to False.
        sso_provider (Optional[SSOProvider]): The SSO provider used by the user, if any. This is optional and can be None if the user does not use SSO.
        sso_id (Optional[str]): The user's ID from the SSO provider. This is optional and can be None if the user does not use SSO.
        last_login (Optional[datetime]): The timestamp of the user's last login. This is optional and can be None if the user has never logged in.

    Class Methods:
        by_email: A class method that takes an email address as input and returns a user document from the database that matches the email address. If no user is found with the provided email, None is returned.
        get_by_sso_id: A class method that takes an SSO provider and an SSO ID as input and returns a user document from the database that matches the SSO provider and SSO ID. If no user is found with the provided SSO provider and SSO ID, None is returned.
    """
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    # is_verified: bool = False
    sso_provider: Optional[SSOProvider] = None
    sso_id: Optional[str] = None
    last_login: Optional[datetime] = None

    @classmethod
    async def by_email(cls, email: EmailStr):
        """
        Retrieve a user document by email address.

        This asynchronous class method queries the database for a user document that matches the given email address.

        Parameters:
            email (EmailStr): The email address to search for in the user documents.

        Returns:
            An instance of the cls (User document) that matches the email address, or None if no match is found.
        """
        return await cls.find_one(cls.email == email)

    @classmethod
    async def get_by_sso_id(cls, provider: SSOProvider, sso_id: str):
        """
        Retrieve a user document by SSO provider and SSO ID.

        This asynchronous class method queries the database for a user document that matches the given SSO provider and SSO ID. This is useful for systems that support single sign-on (SSO) authentication methods.

        Parameters:
            provider (SSOProvider): The SSO provider (e.g., Google, Facebook) used by the user.
            sso_id (str): The unique identifier assigned to the user by the SSO provider.

        Returns:
            An instance of the cls (User document) that matches the SSO provider and SSO ID, or None if no match is found.
        """
        return await cls.find_one((cls.sso_provider == provider) & (cls.sso_id == sso_id))

    async def verify_identity(self) -> bool:
        if self.email_verified and self.verification_status == VerificationStatus.pending:
            self.verification_status = VerificationStatus.verified
            await self.save()
            return True
        return False

    async def initiate_verification(self) -> bool:
        if self.verification_status == VerificationStatus.unverified:
            self.verification_status = VerificationStatus.pending
            # Here you would typically send a verification email
            # For this example, we'll just update the status
            # Refactor this...
            await self.save()
            return True
        return False