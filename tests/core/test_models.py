# tests/test_models.py

import pytest
from datetime import datetime, timedelta
from pydentity.models import User, Agent, Identity, Role, IdentityType, SSOProvider, VerificationStatus

@pytest.mark.asyncio
async def test_user_creation(clear_db):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        identity_type=IdentityType.user
    )
    await user.insert()

    retrieved_user = await User.find_one(User.username == "testuser")
    assert retrieved_user is not None
    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.identity_type == IdentityType.user
    assert retrieved_user.is_active == True
    assert retrieved_user.verification_status == VerificationStatus.unverified

@pytest.mark.asyncio
async def test_agent_creation(clear_db):
    agent = Agent(
        username="testagent",
        api_key="test_api_key",
        identity_type=IdentityType.agent
    )
    await agent.insert()

    retrieved_agent = await Agent.find_one(Agent.username == "testagent")
    assert retrieved_agent is not None
    assert retrieved_agent.api_key == "test_api_key"
    assert retrieved_agent.identity_type == IdentityType.agent

@pytest.mark.asyncio
async def test_user_sso_creation(clear_db):
    user = User(
        username="ssouser",
        email="sso@example.com",
        identity_type=IdentityType.sso_user,
        sso_provider=SSOProvider.google,
        sso_id="google_123456"
    )
    await user.insert()

    retrieved_user = await User.find_one(User.sso_id == "google_123456")
    assert retrieved_user is not None
    assert retrieved_user.sso_provider == SSOProvider.google
    assert retrieved_user.identity_type == IdentityType.sso_user

@pytest.mark.asyncio
async def test_user_verification(clear_db):
    user = User(
        username="verifyuser",
        email="verify@example.com",
        hashed_password="hashed_password",
        identity_type=IdentityType.user
    )
    await user.insert()

    assert user.verification_status == VerificationStatus.unverified
    
    await user.initiate_verification()
    assert user.verification_status == VerificationStatus.pending
    
    user.email_verified = True
    verification_result = await user.verify_identity()
    assert verification_result == True
    assert user.verification_status == VerificationStatus.verified

@pytest.mark.asyncio
async def test_agent_verification(clear_db):
    agent = Agent(
        username="verifyagent",
        api_key="test_api_key",
        identity_type=IdentityType.agent
    )
    await agent.insert()

    assert agent.verification_status == VerificationStatus.unverified
    
    await agent.initiate_verification()
    assert agent.verification_status == VerificationStatus.pending
    assert agent.verification_code is not None
    
    verification_result = await agent.verify_identity()
    assert verification_result == True
    assert agent.verification_status == VerificationStatus.verified
    assert agent.verification_code is None

@pytest.mark.asyncio
async def test_user_role_assignment(clear_db):
    user = User(
        username="roleuser",
        email="role@example.com",
        hashed_password="hashed_password",
        identity_type=IdentityType.user
    )
    await user.insert()

    role = Role(name="admin", permissions=["read", "write", "delete"])
    await role.insert()

    user.roles.append(role)
    await user.save()

    retrieved_user = await User.find_one(User.username == "roleuser")
    assert len(retrieved_user.roles) == 1
    assert retrieved_user.roles[0].name == "admin"
    assert "read" in retrieved_user.roles[0].permissions

@pytest.mark.asyncio
async def test_user_claim_management(clear_db):
    user = User(
        username="claimuser",
        email="claim@example.com",
        hashed_password="hashed_password",
        identity_type=IdentityType.user
    )
    await user.insert()

    await user.add_claim("department", "engineering")
    await user.add_claim("access_level", "high")

    retrieved_user = await User.find_one(User.username == "claimuser")
    assert "department" in retrieved_user.claims
    assert "engineering" in retrieved_user.claims["department"]
    assert "access_level" in retrieved_user.claims
    assert "high" in retrieved_user.claims["access_level"]

    await user.remove_claim("department", "engineering")
    retrieved_user = await User.find_one(User.username == "claimuser")
    assert "department" not in retrieved_user.claims

@pytest.mark.asyncio
async def test_user_last_login_update(clear_db):
    user = User(
        username="loginuser",
        email="login@example.com",
        hashed_password="hashed_password",
        identity_type=IdentityType.user
    )
    await user.insert()

    assert user.last_login is None

    now = datetime.utcnow()
    user.last_login = now
    await user.save()

    retrieved_user = await User.find_one(User.username == "loginuser")
    assert retrieved_user.last_login is not None
    assert (retrieved_user.last_login - now).total_seconds() < 1  # Allow for small time differences

@pytest.mark.asyncio
async def test_agent_last_active_update(clear_db):
    agent = Agent(
        username="activeagent",
        api_key="test_api_key",
        identity_type=IdentityType.agent
    )
    await agent.insert()

    assert agent.last_active is None

    now = datetime.utcnow()
    agent.last_active = now
    await agent.save()

    retrieved_agent = await Agent.find_one(Agent.username == "activeagent")
    assert retrieved_agent.last_active is not None
    assert (retrieved_agent.last_active - now).total_seconds() < 1  # Allow for small time differences