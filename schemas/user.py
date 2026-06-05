from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field

class UserProfile(BaseModel):
    sub: str
    email: Optional[EmailStr] = None
    app_metadata: Dict[str, Any] = Field(default_factory=dict)
    user_metadata: Dict[str, Any] = Field(default_factory=dict)
    aud: Optional[str] = None
    role: str
    role_source: Optional[str] = None
    display_name: Optional[str] = None
    permissions: List[str] = Field(default_factory=list)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
