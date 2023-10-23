from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.dtos.article import ArticleFormData, ArticleImageFormData
from app.repositories.article_repository import ArticleRepository

class ArticleService:
    def __init__(self, db: Session, request: Request = None):
        self.db = db
        self.article_repository = ArticleRepository(db)
        self.base_url = str(request.base_url) if request else ""

    def check_title_exists(self, title: str, exist_article_id : str = False):
        article = self.article_repository.read_article_by_title(title)
        if exist_article_id:
            if article and article.id != exist_article_id:
                raise ValueError("Title already exists")
        else:
            if article:
                raise ValueError("Title already exists")

    def create_article(self, article_form_data: ArticleFormData, image, file_extension):
        return self.article_repository.create_article(article_form_data, image, file_extension)

    def create_article_image(self, article_image_form_data: ArticleImageFormData, image, file_extension):
        return self.article_repository.create_article_image(article_image_form_data, image, file_extension)

    def read_all_article(self, article_status: str, article_lang: str):
        article_datas = []
        articles = self.article_repository.read_all_article(article_status, article_lang)
        if len(articles) > 0:
            for article in articles:
                article_datas.append(
                    {
                        'id': article.id,
                        'title': article.title,
                        'slug': article.slug,
                        'headline': article.headline,
                        'status': article.status,
                        'date': str(article.updated_at),
                        'image': f"{self.base_url}static/articles/image/{article.image_url}" if article.image_url else None,
                    }
                )
        return article_datas

    def read_article(self, article_slug: str):
        content_image_location = f"{self.base_url}static/articles/content/"
        article = self.article_repository.read_article_by_slug(article_slug, content_image_location)
        article_data = {}
        if article:
            article_data['id'] = article.id
            article_data['title'] = article.title
            article_data['slug'] = article.slug
            article_data['headline'] = article.headline
            article_data['status'] = article.status
            article_data['date'] = str(article.updated_at)
            article_data['image'] = f"{self.base_url}static/articles/image/{article.image_url}" if article.image_url else None
            article_data['description'] = article.description

        return article_data

    def update_article(self, article_id:str, article_form_data: ArticleFormData, image, file_extension):
        return self.article_repository.update_article(article_id, article_form_data, image, file_extension)

    def delete_article(self, article_id: str):
        article_id = self.article_repository.delete_article(article_id)
        return article_id

    def delete_article_image(self, article_id: str):
        article = self.article_repository.read_article_by_id(article_id)
        if article and article.status in ('draft', 'flagged'):
            article_id = self.article_repository.delete_article_image(article_id)
            return article_id
        elif not article:
            return ''
        else:
            return 'not allowed'

    def change_article_status(self, article_id: str, article_status: str):
        article = self.article_repository.read_article_by_id(article_id)
        if article:
            article.status = article_status

        return self.article_repository.change_article_status(article)
