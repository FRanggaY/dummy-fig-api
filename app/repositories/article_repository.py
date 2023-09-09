import uuid
import os
from sqlalchemy import asc
from sqlalchemy.orm import Session
from app.dtos.article import ArticleFormData, ArticleImageFormData
from app.models.article import Article, ArticleImage, ArticleStatusParamCustom

from app.utils.handling_file import delete_file, upload_file


class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db
        self.static_folder_thumbnail = "./static/articles/thumbnail/"
        self.static_folder_content = "./static/articles/content/"

    def read_article_by_title(self, title: str) -> Article:
        return self.db.query(Article).filter(Article.title == title).first()

    def create_article(self, article_form_data: ArticleFormData, thumbnail, file_extension):
        file_name = upload_file(thumbnail, self.static_folder_thumbnail, file_extension)

        article_model = Article(id=str(uuid.uuid4()), title=article_form_data.title, headline=article_form_data.headline, slug=article_form_data.slug, description=article_form_data.description, thumbnail_url=file_name, lang=article_form_data.lang)
        self.db.add(article_model)
        self.db.commit()
        self.db.refresh(article_model)
        return article_model

    def create_article_image(self, article_image_form_data: ArticleImageFormData, image, file_extension):
        # handling filename
        file_name = upload_file(image, self.static_folder_content, file_extension)

        # Update the image URL in the database
        article_image_model = ArticleImage(id=str(uuid.uuid4()), article_id=article_image_form_data.article_id, image_url=file_name)
        self.db.add(article_image_model)
        self.db.commit()
        self.db.refresh(article_image_model)

        return article_image_model

    def read_all_article(self, article_status: str, article_lang: str) -> Article:
        if article_status == ArticleStatusParamCustom.all:
            articles = self.db.query(Article.id, Article.title, Article.headline, Article.slug, Article.status, Article.updated_at, Article.thumbnail_url).filter(Article.lang == article_lang).all()
        else:
            articles = self.db.query(Article.id, Article.title, Article.headline, Article.slug, Article.status, Article.updated_at, Article.thumbnail_url).filter(Article.status == article_status, Article.lang == article_lang).all()
        return articles

    def read_article_by_slug(self, article_slug: str, content_image_location: str = False) -> Article:
        article = self.db.query(Article).filter(Article.slug == article_slug).one_or_none()
        if article and content_image_location:
            # initial article image
            article.images = []
            if article:
                article.images = (
                    self.db.query(ArticleImage)
                    .filter(ArticleImage.article_id == article.id)
                    .order_by(asc(ArticleImage.position))
                    .all()
                )

            # handle image to array
            article_images = [article_image.image_url for article_image in article.images]

            # split into array
            description_parts = article.description.split('<img src=\"\">')

            # Use string formatting to insert the image URLs
            formatted_description = ""
            for i, part in enumerate(description_parts):
                formatted_description += part
                if i < len(article_images) and article_images[i]:  # Check if image URL is not empty
                    formatted_description += f'<img src="{content_image_location}{article_images[i]}" alt="image{i + 1}">'

            article.description = formatted_description

        return article

    def read_article_by_id(self, article_id: str) -> Article:
        article = self.db.query(Article).filter(Article.id == article_id).one_or_none()
        return article

    def update_article(self, article_id: str, article_form_data: ArticleFormData, thumbnail, file_extension):
        article = self.read_article_by_id(article_id)

        if not article:
            return ''

        if article.status in ('published', 'archived'):
            return 'not allowed'

        # Delete the existing thumbnail if it exists
        if article.thumbnail_url:
            file_path = os.path.join(self.static_folder_thumbnail, article.thumbnail_url)
            delete_file(file_path)

        # Upload a new thumbnail if provided
        article.thumbnail_url = upload_file(thumbnail, self.static_folder_thumbnail, file_extension)

        # Update article details
        article.title = article_form_data.title
        article.slug = article_form_data.slug
        article.lang = article_form_data.lang

        if article_form_data.headline:
            article.headline = article_form_data.headline

        if article_form_data.description:
            article.description = article_form_data.description

        self.db.commit()
        self.db.refresh(article)
        return article

    def delete_image_of_description(self, article_id: str) -> True:
        # initial article image
        article_content_images = (
            self.db.query(ArticleImage)
            .filter(ArticleImage.article_id == article_id)
            .all()
        )

        # handle image to array
        article_images = [article_image.image_url for article_image in article_content_images]

        for article_image in article_images:
            file_path = os.path.join(self.static_folder_content, article_image)
            delete_file(file_path)

        return True

    def delete_article(self, article_id: str) -> str:
        article = self.db.query(Article).filter(Article.id == article_id).first()

        if not article:
            return ''

        if article.status in ('published', 'archived'):
            return 'not allowed'

        article_id = article.id
        article_thumbnail_url = article.thumbnail_url
        article_description = article.description

        # handle delete thumbnail
        if article_thumbnail_url:
            file_path = os.path.join(self.static_folder_thumbnail, article_thumbnail_url)
            delete_file(file_path)

        # handle delete img of description
        if article_description and '<img' in article_description:
            self.delete_image_of_description(article.id)

        self.db.delete(article)
        self.db.commit()
        return article_id

    def delete_article_image(self, article_id: str) -> str:
        articles = self.db.query(ArticleImage).filter(ArticleImage.article_id == article_id).all()

        if len(articles) > 0:
            self.delete_image_of_description(article_id)

            for article in articles:
                self.db.delete(article)

            self.db.commit()
            return article_id
        else:
            return ''

    def change_article_status(self, article: Article):
        self.db.commit()
        return article
