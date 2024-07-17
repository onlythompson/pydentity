from beanie import Indexed
from pydantic import Field
from typing import Optional
from datetime import datetime

from pydentity.core.models.identity import VerificationStatus

class Agent(Identity):
    """
    Represents an agent entity in the system, extending the Identity model with API key authentication and activity tracking.

    This class is tailored for agents that interact with the system programmatically. It introduces an API key for authentication and tracks the last time the agent was active. Additionally, it includes methods for agent verification, leveraging the system's verification process.

    Attributes:
        api_key (Indexed[str], unique=True): A unique API key assigned to the agent for authentication purposes. The API key must be at least 32 characters long.
        last_active (Optional[datetime]): The timestamp of the agent's last activity in the system. This attribute is used to monitor and potentially audit agent activity.

    Methods:
        by_api_key(cls, api_key: str): A class method to retrieve an agent document from the database based on the provided API key. If no matching agent is found, None is returned.
        verify_identity(self) -> bool: An asynchronous instance method that verifies the agent's identity. This method checks if the agent's verification status is pending and if a verification code is present, then marks the agent as verified.
        initiate_verification(self) -> bool: An asynchronous instance method intended to initiate the verification process for the agent. This method is not implemented and raises NotImplementedError. It's a placeholder for extending the class to support agent verification via a verification code.
        generate_verification_code(self) -> str: Generates a secure verification code for the agent. This method provides a placeholder implementation that generates a 16-character hexadecimal token using the secrets module.

    Note:
        The `verify_identity` and `initiate_verification` methods are part of the agent's verification process. The actual implementation of these methods should be adapted to meet the specific requirements of the system's verification process.
    """
    api_key: Indexed(str, unique=True) = Field(..., min_length=32)
    last_active: Optional[datetime] = None
    verification_code: Optional[str] = None

    @classmethod
    async def by_api_key(cls, api_key: str):
        return await cls.find_one(cls.api_key == api_key)
    
    async def verify_identity(self) -> bool:
        if self.verification_status == VerificationStatus.pending
            # Typically, you would check the verification code here
            self.verification_status = VerificationStatus.verified
            self.verification_code = None
            await self.save()
            return True
        return False

    async def initiate_verification(self) -> bool:
        raise NotImplementedError("Implement Agents verification")
        # if self.verification_status == VerificationStatus.unverified:
        #     self.verification_status = VerificationStatus.pending
        #     # Generate and store a verification code
        #     self.verification_code = self.generate_verification_code()
        #     # Here you would typically send the verification code to the agent owner
        #     await self.save()
        #     return True
        # return False

    def generate_verification_code(self) -> str:
        # Implement a method to generate a secure verification code
        # This is a placeholder implementation
        import secrets
        return secrets.token_hex(16)