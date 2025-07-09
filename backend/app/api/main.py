from fastapi import APIRouter

from app.api.routes import auth
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(auth.router)
