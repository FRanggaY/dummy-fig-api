from typing import Optional
from pydantic import BaseModel, Field

class AuthLogin(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=512)
