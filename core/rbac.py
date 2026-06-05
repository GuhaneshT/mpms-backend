from __future__ import annotations

from collections.abc import Iterable, Mapping
from enum import StrEnum
from typing import Any


class Permission(StrEnum):
    DASHBOARD_READ = "dashboard:read"
    PROFILE_READ = "profile:read"
    CUSTOMERS_READ = "customers:read"
    CUSTOMERS_WRITE = "customers:write"
    ORDERS_READ = "orders:read"
    ORDERS_WRITE = "orders:write"
    ORDER_LIFECYCLE_READ = "order_lifecycle:read"
    ORDER_LIFECYCLE_WRITE = "order_lifecycle:write"
    MACHINES_READ = "machines:read"
    MACHINES_WRITE = "machines:write"
    SERVICE_CALLS_READ = "service_calls:read"
    SERVICE_CALLS_WRITE = "service_calls:write"
    SERVICE_CALLS_RESOLVE = "service_calls:resolve"
    KNOWLEDGE_BASE_READ = "knowledge_base:read"


class AppRole(StrEnum):
    ADMIN = "admin"
    OPERATIONS_MANAGER = "operations_manager"
    SERVICE_MANAGER = "service_manager"
    SERVICE_ENGINEER = "service_engineer"
    VIEWER = "viewer"


RESERVED_SUPABASE_ROLES = {"anon", "authenticated", "service_role"}

ROLE_PERMISSIONS: dict[AppRole, frozenset[Permission]] = {
    AppRole.ADMIN: frozenset(Permission),
    AppRole.OPERATIONS_MANAGER: frozenset(
        {
            Permission.DASHBOARD_READ,
            Permission.PROFILE_READ,
            Permission.CUSTOMERS_READ,
            Permission.CUSTOMERS_WRITE,
            Permission.ORDERS_READ,
            Permission.ORDERS_WRITE,
            Permission.ORDER_LIFECYCLE_READ,
            Permission.ORDER_LIFECYCLE_WRITE,
            Permission.MACHINES_READ,
            Permission.MACHINES_WRITE,
            Permission.SERVICE_CALLS_READ,
            Permission.KNOWLEDGE_BASE_READ,
        }
    ),
    AppRole.SERVICE_MANAGER: frozenset(
        {
            Permission.DASHBOARD_READ,
            Permission.PROFILE_READ,
            Permission.CUSTOMERS_READ,
            Permission.ORDERS_READ,
            Permission.ORDER_LIFECYCLE_READ,
            Permission.ORDER_LIFECYCLE_WRITE,
            Permission.MACHINES_READ,
            Permission.MACHINES_WRITE,
            Permission.SERVICE_CALLS_READ,
            Permission.SERVICE_CALLS_WRITE,
            Permission.SERVICE_CALLS_RESOLVE,
            Permission.KNOWLEDGE_BASE_READ,
        }
    ),
    AppRole.SERVICE_ENGINEER: frozenset(
        {
            Permission.DASHBOARD_READ,
            Permission.PROFILE_READ,
            Permission.ORDERS_READ,
            Permission.ORDER_LIFECYCLE_READ,
            Permission.MACHINES_READ,
            Permission.SERVICE_CALLS_READ,
            Permission.SERVICE_CALLS_WRITE,
            Permission.SERVICE_CALLS_RESOLVE,
            Permission.KNOWLEDGE_BASE_READ,
        }
    ),
    AppRole.VIEWER: frozenset(
        {
            Permission.DASHBOARD_READ,
            Permission.PROFILE_READ,
            Permission.CUSTOMERS_READ,
            Permission.ORDERS_READ,
            Permission.ORDER_LIFECYCLE_READ,
            Permission.MACHINES_READ,
            Permission.SERVICE_CALLS_READ,
            Permission.KNOWLEDGE_BASE_READ,
        }
    ),
}


def _normalize_role(value: Any) -> AppRole | None:
    if not isinstance(value, str):
        return None

    normalized = value.strip().lower()
    if not normalized or normalized in RESERVED_SUPABASE_ROLES:
        return None

    try:
        return AppRole(normalized)
    except ValueError:
        return None


def _claims_section(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    return value if isinstance(value, Mapping) else {}


def resolve_role(payload: Mapping[str, Any]) -> tuple[AppRole, str]:
    app_metadata = _claims_section(payload, "app_metadata")
    user_metadata = _claims_section(payload, "user_metadata")
    candidates = (
        ("app_metadata.rbac_role", app_metadata.get("rbac_role")),
        ("app_metadata.role", app_metadata.get("role")),
        ("user_metadata.role", user_metadata.get("role")),
        ("token.role", payload.get("role")),
    )

    for source, raw_role in candidates:
        role = _normalize_role(raw_role)
        if role:
            return role, source

    return AppRole.VIEWER, "default"


def _coerce_permissions(raw_permissions: Any) -> set[Permission]:
    if isinstance(raw_permissions, str):
        candidates: Iterable[Any] = (raw_permissions,)
    elif isinstance(raw_permissions, Mapping):
        return set()
    elif isinstance(raw_permissions, Iterable):
        candidates = raw_permissions
    else:
        return set()

    permissions: set[Permission] = set()
    for raw_permission in candidates:
        if not isinstance(raw_permission, str):
            continue
        try:
            permissions.add(Permission(raw_permission.strip().lower()))
        except ValueError:
            continue

    return permissions


def resolve_permissions(payload: Mapping[str, Any], role: AppRole) -> list[Permission]:
    app_metadata = _claims_section(payload, "app_metadata")
    user_metadata = _claims_section(payload, "user_metadata")
    permissions = set(ROLE_PERMISSIONS[role])
    permissions.update(_coerce_permissions(app_metadata.get("permissions")))
    permissions.update(_coerce_permissions(user_metadata.get("permissions")))
    permissions.update(_coerce_permissions(payload.get("permissions")))
    return sorted(permissions, key=lambda permission: permission.value)


def build_user_context(payload: Mapping[str, Any]) -> dict[str, Any]:
    role, role_source = resolve_role(payload)
    permissions = resolve_permissions(payload, role)
    user_metadata = _claims_section(payload, "user_metadata")
    display_name = user_metadata.get("full_name") or payload.get("email") or payload.get("sub")

    return {
        **dict(payload),
        "role": role.value,
        "role_source": role_source,
        "permissions": [permission.value for permission in permissions],
        "display_name": display_name,
    }


def has_permission(user: Mapping[str, Any], permission: Permission) -> bool:
    permissions = user.get("permissions") or []
    return permission.value in permissions
