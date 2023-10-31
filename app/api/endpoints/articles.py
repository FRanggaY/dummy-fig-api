from fastapi import APIRouter, Depends, Request, status, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dtos.article import ArticleCreateAndEdit, ArticleFormData, ArticleImageCreate, ArticleImageFormData
from app.models.article import ArticleLangParam, ArticleStatusParamCustom, ArticleStatusParam
from app.models.response import ArticleResponse
from app.models.user import UserStatusParam, UserStatusParamCustom
from app.repositories.article_repository import ArticleRepository
from app.services.article_service import ArticleService
from app.services.user_service import UserService

router = APIRouter()

not_found_message = "Article not found"
result_not_allow = 'not allowed'
status_not_found = 'NOT FOUND'

@router.post("", status_code=status.HTTP_201_CREATED)
def create_article(
    title: str = Form(..., pattern=r'^[a-zA-Z0-9\s]+$'),
    lang: ArticleLangParam = Form(...),
    headline: str = Form(None),
    author: str = Form(None),
    description: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """
        Create a new article
        - validation title unique
        - generate slug from title
    """

    ArticleCreateAndEdit(
        title=title,
        headline=headline,
        description=description,
        author=author,
        image_url=image.filename if image else None,
        lang=lang
    )
    article_service = ArticleService(db)

    try:
        article_service.check_title_exists(title)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    slug = ArticleCreateAndEdit.generate_slug(title)
    article_form = ArticleFormData(title=title, headline=headline, description=description, lang=lang, slug=slug, author=author)

    content_type = image.content_type if image else ""
    file_extension = content_type.split('/')[1] if image else ""
    article_store = article_service.create_article(article_form, image, file_extension)
    status_code = status.HTTP_201_CREATED

    article_response = ArticleResponse(
        code=status_code,
        status="CREATED",
        data={
            'id': article_store.id
        },
    )
    response = JSONResponse(content=article_response.model_dump(), status_code=status_code)
    return response

@router.post("/image", status_code=status.HTTP_201_CREATED)
async def create_article_image(
    article_id: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
        Create a new article of image refer article_id
    """
    ArticleImageCreate(
        article_id=article_id
    )
    article_service = ArticleService(db)

    try:
        await article_service.validation_new_article_images(article_id=article_id, image=image)
    except Exception as e:
        status_code = status.HTTP_400_BAD_REQUEST
        article_response = ArticleResponse(
            code=status_code,
            status="BAD REQUEST",
            data={
                'message': str(e)
            },
        )

        response = JSONResponse(content=article_response.model_dump(), status_code=status_code)
        return response

    article_image_form = ArticleImageFormData(article_id=article_id)

    content_type = image.content_type if image else ""
    file_extension = content_type.split('/')[1] if image else ""
    article_image_store = article_service.create_article_image(article_image_form, image, file_extension)
    status_code = status.HTTP_201_CREATED

    article_response = ArticleResponse(
        code=status_code,
        status="CREATED",
        data={
            'id': article_image_store.id
        },
    )
    response = JSONResponse(content=article_response.model_dump(), status_code=status_code)
    return response

@router.get("", response_model=ArticleResponse, status_code=status.HTTP_200_OK)
def read_all_article(
    request: Request,
    article_status: ArticleStatusParamCustom,
    article_lang: ArticleLangParam,
    db: Session = Depends(get_db),
):
    """
        Read all articles
        - filter by status
        - filter by language
    """
    article_service = ArticleService(db, request)

    articles = article_service.read_all_article(article_status, article_lang)

    if len(articles) == 0:
        status_code = status.HTTP_404_NOT_FOUND
        article_response = ArticleResponse(
            code=status.HTTP_404_NOT_FOUND,
            status=status_not_found,
            data={
                'message': not_found_message
            },
        )
    else:
        status_code = status.HTTP_200_OK
        article_response = ArticleResponse(
            code=status_code,
            status="OK",
            data=articles,
        )
    response = JSONResponse(content=article_response.model_dump(), status_code=status_code)
    return response

@router.get("/{article_slug}", response_model=ArticleResponse, status_code=status.HTTP_200_OK)
def read_article(
    request: Request,
    article_slug: str,
    db: Session = Depends(get_db),
):
    """
        Read articles
        - generate image based description
    """
    article_service = ArticleService(db, request)

    article = article_service.read_article(article_slug)

    if not article:
        status_code = status.HTTP_404_NOT_FOUND
        article_response = ArticleResponse(
            code=status.HTTP_404_NOT_FOUND,
            status=status_not_found,
            data={
                'message': not_found_message
            },
        )
    else:
        status_code = status.HTTP_200_OK
        article_response = ArticleResponse(
            code=status_code,
            status="OK",
            data=article,
        )
    response = JSONResponse(content=article_response.model_dump(), status_code=status_code)
    return response

@router.delete("/{article_id}", response_model=ArticleResponse, status_code=status.HTTP_200_OK)
def delete_article(
    request: Request,
    article_id: str,
    db: Session = Depends(get_db),
):
    """
        Delete article
        - delete existing image in storage
        - delete existing content image in storage
        - only allow delete with status flagged and archived
    """
    article_service = ArticleService(db, request)

    article_id = article_service.delete_article(article_id)

    if article_id == '':
        status_code = status.HTTP_404_NOT_FOUND
        article_response = ArticleResponse(
            code=status.HTTP_404_NOT_FOUND,
            status=status_not_found,
            data={
                'message': not_found_message
            },
        )
    elif article_id == result_not_allow:
        status_code = status.HTTP_403_FORBIDDEN
        article_response = ArticleResponse(
            code=status.HTTP_403_FORBIDDEN,
            status=status_not_found,
            data={
                'message': 'only allow delete with status flagged or archived'
            },
        )
    else:
        status_code = status.HTTP_200_OK
        article_response = ArticleResponse(
            code=status_code,
            status="OK",
            data={
                'id': article_id,
            },
        )
    response = JSONResponse(content=article_response.model_dump(), status_code=status_code)
    return response

@router.put("/{article_id}/status", response_model=ArticleResponse, status_code=status.HTTP_200_OK)
def change_article_status(
    request: Request,
    article_id: str,
    article_status: ArticleStatusParam,
    db: Session = Depends(get_db),
):
    """
        Change article status
    """
    article_service = ArticleService(db, request)

    article = article_service.change_article_status(article_id, article_status)

    if article == '' or not article:
        status_code = status.HTTP_404_NOT_FOUND
        article_response = ArticleResponse(
            code=status.HTTP_404_NOT_FOUND,
            status=status_not_found,
            data={
                'message': not_found_message
            },
        )
    else:
        status_code = status.HTTP_200_OK
        article_response = ArticleResponse(
            code=status_code,
            status="OK",
            data={
                'id': article.id,
            },
        )
    response = JSONResponse(content=article_response.model_dump(), status_code=status_code)
    return response

@router.patch("/{article_id}", response_model=ArticleResponse, status_code=status.HTTP_200_OK)
def update_article(
    request: Request,
    article_id: str,
    title: str = Form(..., pattern=r'^[a-zA-Z0-9\s]+$'),
    lang: ArticleLangParam = Form(...),
    headline: str = Form(None),
    description: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    """
        Update article
        - validation existing title
        - validation title allow when article it itself
        - delete a existing thumnail and replace with new if new image is provided
        - only allow to update with status flagged or draft
    """
    article_service = ArticleService(db, request)

    ArticleCreateAndEdit(
        title=title,
        headline=headline,
        description=description,
        image_url=image.filename if image else None,
        lang=lang
    )

    article_service = ArticleService(db)

    try:
        article_service.check_title_exists(title, article_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    slug = ArticleCreateAndEdit.generate_slug(title)
    article_form = ArticleFormData(title=title, headline=headline, description=description, lang=lang, slug=slug)

    content_type = image.content_type if image else ""
    file_extension = content_type.split('/')[1] if image else ""
    article_update = article_service.update_article(article_id, article_form, image, file_extension)

    if article_update == '':
        status_code = status.HTTP_404_NOT_FOUND
        article_response = ArticleResponse(
            code=status.HTTP_404_NOT_FOUND,
            status=status_not_found,
            data={
                'message': not_found_message
            },
        )
    elif article_update == result_not_allow:
        status_code = status.HTTP_403_FORBIDDEN
        article_response = ArticleResponse(
            code=status.HTTP_403_FORBIDDEN,
            status=status_not_found,
            data={
                'message': 'only allow delete with status flagged or draft'
            },
        )
    else:
        status_code = status.HTTP_200_OK
        article_response = ArticleResponse(
            code=status_code,
            status="OK",
            data={
                'id': article_update.id,
            },
        )
    response = JSONResponse(content=article_response.model_dump(), status_code=status_code)
    return response

@router.delete("/{article_id}/image", response_model=ArticleResponse, status_code=status.HTTP_200_OK)
def delete_article_image(
    request: Request,
    article_id: str,
    db: Session = Depends(get_db),
):
    """
        Update article image
        - delete a all data refer article_id with existing file too
        - only allow to delete with status draft or flagged
    """
    article_service = ArticleService(db, request)

    article_id = article_service.delete_article_image(article_id)
    if article_id == '':
        status_code = status.HTTP_404_NOT_FOUND
        article_response = ArticleResponse(
            code=status.HTTP_404_NOT_FOUND,
            status=status_not_found,
            data={
                'message': not_found_message
            },
        )
    elif article_id == result_not_allow:
        status_code = status.HTTP_403_FORBIDDEN
        article_response = ArticleResponse(
            code=status.HTTP_403_FORBIDDEN,
            status="FORBIDDEN",
            data={
                'message': 'only allow delete with status flagged or archived'
            },
        )
    else:
        status_code = status.HTTP_200_OK
        article_response = ArticleResponse(
            code=status_code,
            status="OK",
            data={
                'id': article_id,
            },
        )
    response = JSONResponse(content=article_response.model_dump(), status_code=status_code)
    return response
