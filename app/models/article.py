import uuid
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Enum, String, ForeignKey, Integer, func
from sqlalchemy.orm import relationship
from enum import Enum as EnumParam

from app.database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(50), unique=True, nullable=False)
    slug = Column(String(60), unique=True, nullable=False)
    headline = Column(String(1024), nullable=True)
    description = Column(String(2048), nullable=True)
    thumbnail_url = Column(String(512), nullable=True)
    status = Column(Enum('draft', 'flagged', 'archived', 'publish'), server_default='draft', nullable=False)
    lang = Column(Enum('eng', 'ind'), server_default='ind', nullable=False)
    created_at = Column(DateTime, server_default=func.NOW(), nullable=False)
    updated_at = Column(DateTime, server_default=func.NOW(), onupdate=func.NOW(), nullable=False)

    article_images = relationship('ArticleImage', back_populates='article', cascade='all, delete')

class ArticleImage(Base):
    __tablename__ = "article_images"

    id = Column(String, primary_key=True, index=True)
    article_id = Column(ForeignKey('articles.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    image_url = Column(String(512), nullable=True)
    position = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.NOW(), nullable=False)
    updated_at = Column(DateTime, server_default=func.NOW(), onupdate=func.NOW(), nullable=False)

    article = relationship('Article', back_populates='article_images')

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
    eng = "eng"
    ind = "ind"
