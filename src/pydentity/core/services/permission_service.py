# src/pyidentity/core/services/permission_service.py

from pyidentity.core.models import Identity, Role

class PermissionService:
    async def create_role(self, name: str, permissions: list[str], description: str = None):
        role = Role(name=name, permissions=permissions, description=description)
        await role.insert()
        return role

    async def add_permission_to_role(self, role: Role, permission: str):
        if permission not in role.permissions:
            role.permissions.append(permission)
            await role.save()

    async def remove_permission_from_role(self, role: Role, permission: str):
        if permission in role.permissions:
            role.permissions.remove(permission)
            await role.save()

    async def check_permission(self, identity: Identity, permission: str):
        return await identity.has_permission(permission)
