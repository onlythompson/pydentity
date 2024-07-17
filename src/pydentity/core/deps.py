"""Dependency injection for services."""

from fastapi import Depends
from .services import AuthService, IdentityService, PermissionService, TokenService

def get_auth_service(token_service: TokenService = Depends()):
    return AuthService(token_service)

def get_identity_service(auth_service: AuthService = Depends(get_auth_service)):
    return IdentityService(auth_service)

def get_permission_service():
    return PermissionService()

def get_token_service():
    return TokenService()

def get_current_identity(auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.get_current_identity()