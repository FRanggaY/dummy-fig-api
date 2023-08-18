from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dtos.auth import AuthLogin
from app.models.response import AuthResponse
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def auth_login(auth_login: AuthLogin, db: Session = Depends(get_db)):
    """
        Login user
        - check username exist
        - check password correction
    """
    auth_service = AuthService(db)

    try:
        auth_data = auth_service.auth_login(auth_login)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    user_response = AuthResponse(
        code=status.HTTP_200_OK,
        status="OK",
        data={
            'id': auth_data.get('user_id', None),
            'access_token': auth_data.get('access_token', None),
            'refresh_token': auth_data.get('refresh_token', None),
            'expired_at': auth_data.get('access_token_expired_at', None)
        },
    )
    return user_response

# @router.post("/refresh-token", response_model=AuthResponse, status_code=status.HTTP_200_OK)
# def auth_refresh_token(db: Session = Depends(get_db)):
#     """
#         Refresh token user

#         COMING SOON
#     """
#     pass

# @router.post("/logout", response_model=AuthResponse, status_code=status.HTTP_200_OK)
# def auth_logout(db: Session = Depends(get_db)):
#     """
#         Logout user

#         COMING SOON
#         - refer with saving refresh token
#     """
#     pass

# @router.post("/profile", response_model=AuthResponse, status_code=status.HTTP_200_OK)
# def auth_profile(db: Session = Depends(get_db)):
#     """
#         Profile user

#         COMING SOON
#         - refer with active login from token
#     """
#     pass
