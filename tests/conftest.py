# tests/conftest.py

import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pydentity.core.config import get_settings
from pydentity.models import User, Agent, Identity, Role

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def db():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.TEST_MONGODB_URL)
    await init_beanie(database=client[settings.TEST_MONGODB_DB_NAME], document_models=[User, Agent, Identity, Role])
    yield
    await client.drop_database(settings.TEST_MONGODB_DB_NAME)
    client.close()

@pytest.fixture
async def clear_db(db):
    yield
    await User.delete_all()
    await Agent.delete_all()
    await Role.delete_all()