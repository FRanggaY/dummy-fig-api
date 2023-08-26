import uuid
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Enum, String, func
from enum import Enum as EnumParam

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    hashed_password = Column(String(512), nullable=False)
    status = Column(Enum('active', 'inactive', 'idle'), server_default='inactive', nullable=False)
    email_verified_at = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.NOW(), nullable=False)
    updated_at = Column(DateTime, server_default=func.NOW(), onupdate=func.NOW(), nullable=False)

class UserStatusParam(str, EnumParam):
    active = "active"
    inactive = "inactive"
    idle = "idle"

class UserStatusParamCustom(str, EnumParam):
    all = "all"
    active = "active"
    inactive = "inactive"
    idle = "idle"
