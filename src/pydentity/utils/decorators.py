# src/pyidentity/utils/decorators.py

from functools import wraps
from fastapi import HTTPException, Depends
from typing import Dict, List, Union
from pyidentity.core.models import Identity, User, Agent
from pyidentity.core.services import get_current_identity

def require_permissions(permissions: Union[str, List[str]]):
    if isinstance(permissions, str):
        permissions = [permissions]

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_identity: Identity = Depends(get_current_identity), **kwargs):
            for permission in permissions:
                if not await current_identity.has_permission(permission):
                    raise HTTPException(status_code=403, detail=f"Permission denied: {permission}")
            return await func(*args, current_identity=current_identity, **kwargs)
        return wrapper
    return decorator

def require_any_permission(permissions: List[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_identity: Identity = Depends(get_current_identity), **kwargs):
            for permission in permissions:
                if await current_identity.has_permission(permission):
                    return await func(*args, current_identity=current_identity, **kwargs)
            raise HTTPException(status_code=403, detail="Permission denied")
        return wrapper
    return decorator

def require_identity_type(allowed_types: Union[IdentityType, List[IdentityType]]):
    if isinstance(allowed_types, IdentityType):
        allowed_types = [allowed_types]

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_identity: Identity = Depends(get_current_identity), **kwargs):
            if current_identity.identity_type not in allowed_types:
                raise HTTPException(status_code=403, detail="Invalid identity type")
            return await func(*args, current_identity=current_identity, **kwargs)
        return wrapper
    return decorator

""" Claims-based decorators """
def require_claims(claims: Dict[str, Union[str, List[str]]]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_identity: Identity = Depends(get_current_identity), **kwargs):
            for claim_type, claim_values in claims.items():
                if isinstance(claim_values, str):
                    claim_values = [claim_values]
                if claim_type not in current_identity.claims or not any(value in current_identity.claims[claim_type] for value in claim_values):
                    raise HTTPException(status_code=403, detail=f"Required claim not found: {claim_type}")
            return await func(*args, current_identity=current_identity, **kwargs)
        return wrapper
    return decorator

def require_any_claim(claims: Dict[str, Union[str, List[str]]]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_identity: Identity = Depends(get_current_identity), **kwargs):
            for claim_type, claim_values in claims.items():
                if isinstance(claim_values, str):
                    claim_values = [claim_values]
                if claim_type in current_identity.claims and any(value in current_identity.claims[claim_type] for value in claim_values):
                    return await func(*args, current_identity=current_identity, **kwargs)
            raise HTTPException(status_code=403, detail="Required claims not found")
        return wrapper
    return decorator