from fastapi import File, Request, Depends
from sqlalchemy.orm import Session
from app.dtos.article import ArticleCategoryAssignAndUnassignFormData, ArticleCategoryFormData, ArticleFormData, ArticleImageFormData
from app.repositories.article_repository import ArticleRepository

class ArticleService:
    def __init__(self, db: Session, request: Request = None):
        self.db = db
        self.article_repository = ArticleRepository(db)
        self.base_url = str(request.base_url) if request else ""

    def check_exists(self, function, exist_id, label):
        data = function
        if exist_id:
            if data and data.id != exist_id:
                raise ValueError(f"{label} already exists")
        else:
            if data:
                raise ValueError(f"{label} already exists")

    def check_title_exists(self, title: str, exist_article_id : str = False):
        self.check_exists(function=self.article_repository.read_article_by_title(title), exist_id=exist_article_id, label='Title')

    def check_category_label_exists(self, label: str, exist_category_id : str = False):
        self.check_exists(function=self.article_repository.read_category_by_label(label), exist_id=exist_category_id, label='Label')

    def check_article_category_assigned(self, article_id: str, category_id : str):
        category = self.article_repository.read_article_category_by_article_id_and_category_id(article_id, category_id)
        if category:
            raise ValueError("Category already assigned")

    async def validation_new_article_images(self, article_id: str, image: File, limit_file_size_mb: int = 5, allowed_extension: list = ["image/jpeg", "image/png"]):
        article_id_valid = self.article_repository.read_article_by_id(article_id=article_id)
        if not article_id_valid:
            raise ValueError("Article not found")

        image.file.seek(0, 2)
        file_size = image.file.tell()

        # move the cursor back to the beginning
        await image.seek(0)
        if file_size > limit_file_size_mb * 1024 * 1024:
            # more than 5 MB
            raise ValueError(f"Image too large. only allow image lower than {limit_file_size_mb} mb")

        # check the content type (MIME type)
        content_type = image.content_type
        if content_type not in allowed_extension:
            image_formats = ', '.join([mime.split('/')[-1] for mime in allowed_extension])
            raise ValueError(f"Invalid image file type. only allow image with type {image_formats}")

    def create_article(self, article_form_data: ArticleFormData, image, file_extension):
        return self.article_repository.create_article(article_form_data, image, file_extension)

    def create_article_category(self, article_category_form_data: ArticleCategoryFormData):
        return self.article_repository.create_article_category(article_category_form_data)

    def create_article_image(self, article_image_form_data: ArticleImageFormData, image, file_extension):
        return self.article_repository.create_article_image(article_image_form_data, image, file_extension)

    def read_all_article(self, article_status: str, article_lang: str, category_id: str = None, offset: int = None, limit: int = None):
        article_datas = []
        results = self.article_repository.read_all_article(article_status, article_lang, category_id, offset, limit)
        articles = results['articles']
        total_article = results['total_article']

        if len(articles) > 0:
            for article in articles:
                category_values = [{'id': article_category.category.id, 'value': article_category.category.label} for article_category in article.article_categories]
                category_datas = category_values if category_values else []
                article_datas.append(
                    {
                        'id': article.id,
                        'title': article.title,
                        'slug': article.slug,
                        'headline': article.headline,
                        'status': article.status,
                        'categories': category_datas,
                        'published_at': str(article.published_at) if article.published_at else None,
                        'updated_at': str(article.updated_at) if article.updated_at else None,
                        'image': f"{self.base_url}static/articles/image/{article.image_url}" if article.image_url else None,
                    }
                )
        return article_datas, total_article

    def read_all_article_category(self):
        article_category_datas = []
        article_categories = self.article_repository.read_all_article_category()
        if len(article_categories) > 0:
            for article_category in article_categories:
                article_category_datas.append(
                    {
                        'id': article_category.id,
                        'label': article_category.label,
                    }
                )
        return article_category_datas

    def read_article(self, article_slug: str):
        content_image_location = f"{self.base_url}static/articles/content/"
        article = self.article_repository.read_article_by_slug(article_slug, content_image_location)
        category_values = [{'id': article_category.category.id, 'value': article_category.category.label} for article_category in article.article_categories]
        category_datas = category_values if category_values else []
        article_data = {}
        if article:
            article_data['id'] = article.id
            article_data['title'] = article.title
            article_data['slug'] = article.slug
            article_data['headline'] = article.headline
            article_data['status'] = article.status
            article_data['image'] = f"{self.base_url}static/articles/image/{article.image_url}" if article.image_url else None
            article_data['description'] = article.description
            article_data['published_at'] = str(article.published_at) if article.published_at else None
            article_data['updated_at'] = str(article.updated_at) if article.updated_at else None
            article_data['categories'] = category_datas
            article_data['author'] = article.author

        return article_data

    def update_article(self, article_id:str, article_form_data: ArticleFormData, image, file_extension):
        return self.article_repository.update_article(article_id, article_form_data, image, file_extension)

    def delete_article(self, article_id: str):
        article_id = self.article_repository.delete_article(article_id)
        return article_id

    def delete_article_category(self, category_id: str):
        category_id = self.article_repository.delete_article_category(category_id)
        return category_id

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

    def assign_article_category(self, article_id: str, category_id: str):
        article = self.article_repository.read_article_by_id(article_id)
        article_category = self.article_repository.read_article_category_by_id(category_id)
        if not article or not article_category:
            return ''

        # check that already assigned category or not
        article_category_exist = self.check_article_category_assigned(article_id, category_id)
        if article_category_exist:
            return 'already assigned'

        article_category_assign_and_unassign_model = ArticleCategoryAssignAndUnassignFormData(article_id=article_id, category_id=category_id)
        return self.article_repository.assign_article_category(article_category_assign_and_unassign_model)

    def unassign_article_category(self, article_id: str, category_id: str):
        article_category_assign_and_unassign_model = ArticleCategoryAssignAndUnassignFormData(article_id=article_id, category_id=category_id)
        return self.article_repository.unassign_article_category(article_category_assign_and_unassign_model)
