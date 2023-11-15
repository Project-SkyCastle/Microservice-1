from pydantic import BaseModel, validator
from enum import Enum
from datetime import datetime
from typing import Optional


class Role(str, Enum):
    CLIENT = "CLIENT"
    ANALYST = "ANALYST"
    ADMIN = "ADMIN"


class User(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    created: Optional[datetime] = None
    role: Optional[str] = None
    discord_url: Optional[str] = None

    @validator("role")
    def role_is_valid(cls, role):
        color_values = set(item.value for item in Role)
        if role in color_values:
            return role
        raise RuntimeError(f"Invalid role: {role}")
