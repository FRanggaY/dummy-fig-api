from fastapi import APIRouter, Depends, status, HTTPException
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

    user_response = UserResponse(
        code=status.HTTP_201_CREATED,
        status="CREATED",
        data={
            'id': user_store.id
        },
    )
    return user_response

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
        user_response = UserResponse(
            code=status.HTTP_404_NOT_FOUND,
            status="NOT FOUND",
            data={
                'message': "Users not found"
            },
        )
    else:
        user_response = UserResponse(
            code=status.HTTP_200_OK,
            status="OK",
            data=users,
        )
    return user_response

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
        user_response = UserResponse(
            code=status.HTTP_404_NOT_FOUND,
            status="NOT FOUND",
            data={
                'message': not_found_message
            },
        )
    else:
        user_response = UserResponse(
            code=status.HTTP_200_OK,
            status="OK",
            data={
                'id': user.id,
                'username': user.username,
                'status': user.status
            },
        )
    return user_response

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
        user_response = UserResponse(
            code=status.HTTP_404_NOT_FOUND,
            status="NOT FOUND",
            data={
                'message': not_found_message
            },
        )
    else:
        user_response = UserResponse(
            code=status.HTTP_200_OK,
            status="OK",
            data={
                'id': user.id,
            },
        )
    return user_response

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
        user_response = UserResponse(
            code=status.HTTP_404_NOT_FOUND,
            status="NOT FOUND",
            data={
                'message': not_found_message
            },
        )
    else:
        user_response = UserResponse(
            code=status.HTTP_200_OK,
            status="OK",
            data={
                'id': user_id,
            },
        )
    return user_response
