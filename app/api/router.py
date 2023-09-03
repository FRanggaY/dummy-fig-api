from fastapi import APIRouter
from .endpoints import users, auth, articles

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(articles.router, prefix="/articles", tags=["Articles"])
