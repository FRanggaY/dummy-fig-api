from typing import Optional
from pydantic import BaseModel, Field, constr
from app.models.article import Article, ArticleLangParam

from app.models.user import UserStatusParam

class ArticleCreateAndEdit(BaseModel):
    title: constr(min_length=1, max_length=50)
    headline: Optional[constr(min_length=1, max_length=1024)]
    description: Optional[constr(min_length=1, max_length=2048)]
    image_url: Optional[constr(min_length=1, max_length=512)]
    lang: str

    @classmethod
    def generate_slug(cls, title):
        slug = title.lower().replace(' ', '-')
        return slug

    @classmethod
    def validate_title(cls, title):
        exists = Article.where(Article.title == title).exists()
        if exists:
            raise ValueError("Title already exists")

class ArticleImageCreate(BaseModel):
    article_id: constr(min_length=1, max_length=50)

class ArticleFormData(BaseModel):
    title: str
    headline: Optional[str]
    description: Optional[str]
    slug: str
    lang: str

class ArticleImageFormData(BaseModel):
    article_id: str
