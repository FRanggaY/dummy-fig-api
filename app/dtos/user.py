from typing import Optional
from pydantic import BaseModel, Field

from app.models.user import UserStatusParam

class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=1, max_length=512)

class UserEdit(BaseModel):
    status: UserStatusParam = Field(...)
    password: Optional[str] = Field(None, min_length=1, max_length=512)
    username: str = Field(None, min_length=1, max_length=50)
    email: str = Field(None, min_length=1, max_length=50)
