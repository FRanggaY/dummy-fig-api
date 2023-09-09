from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dtos.user import UserCreate, UserEdit
from app.models.response import UserResponse
from app.models.user import UserStatusParam, UserStatusParamCustom
from app.services.user_service import UserService

router = APIRouter()

not_found_message =  "User not found"

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    """
        Create a new user
        - validation unique username
        - validation unique email
    """
    user_service = UserService(db)

    try:
        user_service.check_username_exists(user_create.username)
        user_service.check_email_exists(user_create.email)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    user_store = user_service.create_user(user_create)

    status_code = status.HTTP_201_CREATED
    user_response = UserResponse(
        code=status_code,
        status="CREATED",
        data={
            'id': user_store.id
        },
    )
    response = JSONResponse(content=user_response.model_dump(), status_code=status_code)
    return response

@router.get("", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_all_user(
    user_status: UserStatusParamCustom,
    db: Session = Depends(get_db)
):
    """
        Read all users
    """
    user_service = UserService(db)

    users = user_service.read_all_user(user_status)

    if len(users) == 0:
        status_code = status.HTTP_404_NOT_FOUND
        user_response = UserResponse(
            code=status_code,
            status="NOT FOUND",
            data={
                'message': "Users not found"
            },
        )
    else:
        status_code = status.HTTP_200_OK
        user_response = UserResponse(
            code=status_code,
            status="OK",
            data=users,
        )
    response = JSONResponse(content=user_response.model_dump(), status_code=status_code)
    return response

@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_user(
    id: str,
    db: Session = Depends(get_db)
):
    """
        Read user
    """
    user_service = UserService(db)

    user = user_service.read_user(id)

    if user is None:
        status_code = status.HTTP_404_NOT_FOUND
        user_response = UserResponse(
            code=status_code,
            status="NOT FOUND",
            data={
                'message': not_found_message
            },
        )
    else:
        status_code = status.HTTP_200_OK
        user_response = UserResponse(
            code=status_code,
            status="OK",
            data={
                'id': user.id,
                'username': user.username,
                'status': user.status
            },
        )
    response = JSONResponse(content=user_response.model_dump(), status_code=status_code)
    return response

@router.patch("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(id: str, user_edit: UserEdit, db: Session = Depends(get_db)):
    """
        Update user
        - validation unique username
        - validation unique email
    """
    user_service = UserService(db)

    try:
       user_service.check_username_exists(user_edit.username)
       user_service.check_email_exists(user_edit.email)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    user = user_service.update_user(user_edit, id)

    if user == '':
        status_code = status.HTTP_404_NOT_FOUND
        user_response = UserResponse(
            code=status_code,
            status="NOT FOUND",
            data={
                'message': not_found_message
            },
        )
    else:
        status_code = status.HTTP_200_OK
        user_response = UserResponse(
            code=status_code,
            status="OK",
            data={
                'id': user.id,
            },
        )
    response = JSONResponse(content=user_response.model_dump(), status_code=status_code)
    return response

@router.delete("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def delete_user(
    id: str,
    db: Session = Depends(get_db)
):
    """
        Delete user
    """
    user_service = UserService(db)

    user_id = user_service.delete_user(id)

    if user_id == '':
        status_code = status.HTTP_404_NOT_FOUND
        user_response = UserResponse(
            code=status_code,
            status="NOT FOUND",
            data={
                'message': not_found_message
            },
        )
    else:
        status_code = status.HTTP_200_OK
        user_response = UserResponse(
            code=status_code,
            status="OK",
            data={
                'id': user_id,
            },
        )
    response = JSONResponse(content=user_response.model_dump(), status_code=status_code)
    return response
