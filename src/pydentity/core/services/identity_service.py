"""Identity Service Module."""

from pydentity.core.models import Identity, User, Agent, Role
from pydentity.core.schemas import UserCreate, AgentCreate
from .auth_service import AuthService
from fastapi import Depends

class IdentityService:
    def __init__(self, auth_service: AuthService = Depends()):
        self.auth_service = auth_service

    async def create_user(self, user_create: UserCreate):
        hashed_password = self.auth_service.get_password_hash(user_create.password)
        user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            identity_type="user"
        )
        await user.insert()
        return user

    async def create_agent(self, agent_create: AgentCreate):
        agent = Agent(
            username=agent_create.username,
            api_key=agent_create.api_key,
            identity_type="agent"
        )
        await agent.insert()
        return agent

    async def get_identity(self, username: str):
        return await Identity.find_one(Identity.username == username)

    async def add_role_to_identity(self, identity: Identity, role: Role):
        if role not in identity.roles:
            identity.roles.append(role)
            await identity.save()

    async def remove_role_from_identity(self, identity: Identity, role: Role):
        if role in identity.roles:
            identity.roles.remove(role)
            await identity.save()
