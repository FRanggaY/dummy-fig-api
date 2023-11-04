from typing import Optional
from pydantic import BaseModel, Field, constr
from app.models.article import Article, ArticleLangParam
from app.models.category import Category

from app.models.user import UserStatusParam

class ArticleCategoryCreate(BaseModel):
    label: constr(min_length=1, max_length=50)

    @classmethod
    def validate_label(cls, label):
        exists = Category.where(Category.label == label).exists()
        if exists:
            raise ValueError("Label already exists")

class ArticleCreateAndEdit(BaseModel):
    title: constr(min_length=1, max_length=50)
    headline: Optional[constr(min_length=1, max_length=1024)]
    author: Optional[constr(min_length=1, max_length=512)]
    description: Optional[constr(min_length=1, max_length=2048)]
    author: Optional[constr(min_length=1, max_length=512)]
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
    author: Optional[str]
    slug: str
    lang: str

class ArticleImageFormData(BaseModel):
    article_id: str

class ArticleCategoryAssignAndUnassignFormData(BaseModel):
    article_id: str
    category_id: str

class ArticleCategoryFormData(BaseModel):
    label: str
