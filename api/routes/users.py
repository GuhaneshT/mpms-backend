from fastapi import APIRouter, Depends
from backend.api.deps import get_current_user
from backend.schemas.user import UserProfile

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserProfile)
def get_me(current_user: dict = Depends(get_current_user)):
    """
    Returns the current authenticated user's profile from the JWT payload.
    """
    return current_user
