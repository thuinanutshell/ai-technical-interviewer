import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# App configuration based on environment
app_config = {
    "title": "AI Technical Interviewer",
    "version": "0.1.0",
}

# Add debug info for non-production
if not settings.is_production:
    app_config.update(
        {"docs_url": "/docs", "redoc_url": "/redoc", "openapi_url": "/openapi.json"}
    )
else:
    # Disable docs in production for security
    app_config.update({"docs_url": None, "redoc_url": None, "openapi_url": None})

app = FastAPI(**app_config)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {
        "message": "AI Technical Interviewer API",
        "environment": settings.ENVIRONMENT,
        "version": app_config["version"],
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


# Log startup info
logger.info(f"Starting application in {settings.ENVIRONMENT} environment")
if settings.is_development:
    logger.info("Development mode: API docs available at /docs")
