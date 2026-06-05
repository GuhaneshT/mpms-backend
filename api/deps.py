from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from collections.abc import Mapping
from core.security import verify_token
from core.rbac import Permission, build_user_context, has_permission

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependency to get the current authenticated user via Supabase JWT.
    """
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid auth token payload")

    return build_user_context(payload)


def require_permissions(*required_permissions: Permission):
    def dependency(current_user: dict = Depends(get_current_user)) -> dict:
        missing_permissions = [
            permission.value
            for permission in required_permissions
            if not has_permission(current_user, permission)
        ]
        if missing_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "You do not have permission to access this resource.",
                    "missing_permissions": missing_permissions,
                },
            )
        return current_user

    return dependency


def user_has_permission(current_user: Mapping[str, object], permission: Permission) -> bool:
    return has_permission(current_user, permission)
