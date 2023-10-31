import uuid
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Enum, String, ForeignKey, Integer, func, Date
from sqlalchemy.orm import relationship
from enum import Enum as EnumParam

from app.database import Base
from app.models.category import Category

class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(50), unique=True, nullable=False)
    slug = Column(String(60), unique=True, nullable=False)
    headline = Column(String(1024), nullable=True)
    description = Column(String(2048), nullable=True)
    image_url = Column(String(512), nullable=True)
    author = Column(String(128), nullable=True)
    status = Column(Enum('draft', 'flagged', 'archived', 'publish'), server_default='draft', nullable=False)
    lang = Column(Enum('en', 'id'), server_default='en', nullable=False)
    published_at = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.NOW(), nullable=False)
    updated_at = Column(DateTime, server_default=func.NOW(), onupdate=func.NOW(), nullable=False)

    article_images = relationship('ArticleImage', back_populates='article', cascade='all, delete')
    article_categories = relationship('ArticleCategory', back_populates='article', cascade='all, delete')

class ArticleImage(Base):
    __tablename__ = "article_images"

    id = Column(String, primary_key=True, index=True)
    article_id = Column(ForeignKey('articles.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    image_url = Column(String(512), nullable=True)
    position = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.NOW(), nullable=False)
    updated_at = Column(DateTime, server_default=func.NOW(), onupdate=func.NOW(), nullable=False)

    article = relationship('Article', back_populates='article_images')

class ArticleCategory(Base):
    __tablename__ = "article_categories"

    id = Column(String(36), primary_key=True, index=True)
    article_id = Column(ForeignKey('articles.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    category_id = Column(ForeignKey('categories.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.NOW(), nullable=False)
    updated_at = Column(DateTime, server_default=func.NOW(), onupdate=func.NOW(), nullable=False)

    article = relationship('Article', back_populates='article_categories')
    category = relationship('Category', back_populates='article_categories')

class ArticleStatusParam(str, EnumParam):
    draft = "draft"
    flagged = "flagged"
    archived = "archived"
    publish = "publish"

class ArticleStatusParamCustom(str, EnumParam):
    all = "all"
    draft = "draft"
    flagged = "flagged"
    archived = "archived"
    publish = "publish"

class ArticleLangParam(str, EnumParam):
    en = "en"
    id = "id"
