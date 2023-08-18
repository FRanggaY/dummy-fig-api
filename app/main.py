from fastapi import FastAPI
from app.config import config
from app.api.router import router as api_router
from app.database import Base, engine

# Create the FastAPI app instance
app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
)

# Include the API router
app.include_router(api_router, prefix="/api/v1")
