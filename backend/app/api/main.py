from fastapi import APIRouter

from app.api.routes import auth, resume, interview, questions
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(resume.router)
api_router.include_router(interview.router)
api_router.include_router(questions.router)
