from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class UserProfile(BaseModel):
    sub: str
    email: EmailStr
    app_metadata: Dict[str, Any]
    user_metadata: Dict[str, Any]
    aud: str
    role: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
