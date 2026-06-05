from fastapi import APIRouter, Depends
from api.deps import require_permissions
from core.rbac import Permission
from schemas.user import UserProfile

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserProfile)
def get_me(current_user: dict = Depends(require_permissions(Permission.PROFILE_READ))):
    """
    Returns the current authenticated user's profile from the JWT payload.
    """
    return current_user
