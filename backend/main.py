from fastapi import FastAPI

from api.router import api_router
from config.settings import settings
from core.errors import register_exception_handlers
from core.middleware import register_middleware


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    register_middleware(app)
    register_exception_handlers(app)
    app.include_router(api_router)

    return app


app = create_app()
