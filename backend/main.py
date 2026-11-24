import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from api.router import api_router
from config.settings import settings
from core.errors import register_exception_handlers
from core.middleware import register_middleware
from db.database import (
    SessionLocal,
    check_database_connection,
    close_database,
    initialize_database,
)
from services.session_memory_service import SessionMemoryService

logger = logging.getLogger(__name__)


def purge_expired_session_memory() -> int:
    with SessionLocal() as db_session:
        return SessionMemoryService(db_session).purge_expired_sessions()


async def cleanup_expired_session_memory(database_ready: bool) -> None:
    while True:
        await asyncio.sleep(settings.session_memory_cleanup_interval_seconds)
        try:
            if not database_ready:
                await asyncio.to_thread(initialize_database)
                database_ready = True
            await asyncio.to_thread(purge_expired_session_memory)
        except SQLAlchemyError:
            database_ready = False
            logger.exception("Could not purge expired session memory")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    del app
    database_ready = False
    try:
        check_database_connection()
        initialize_database()
        database_ready = True
        logger.info("Database connection established")
    except Exception as exc:
        logger.warning("Database is unavailable at startup: %s", exc)
    cleanup_task = asyncio.create_task(cleanup_expired_session_memory(database_ready))
    try:
        yield
    finally:
        cleanup_task.cancel()
        try:
            await cleanup_task
        except asyncio.CancelledError:
            pass
        close_database()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    register_middleware(app)
    register_exception_handlers(app)
    app.include_router(api_router)

    return app


app = create_app()
