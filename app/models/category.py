import uuid
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Enum, String, ForeignKey, Integer, func, Date
from sqlalchemy.orm import relationship
from enum import Enum as EnumParam

from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(String(36), primary_key=True, index=True)
    label = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.NOW(), nullable=False)
    updated_at = Column(DateTime, server_default=func.NOW(), onupdate=func.NOW(), nullable=False)

    article_categories = relationship('ArticleCategory', back_populates='category', cascade='all, delete')


