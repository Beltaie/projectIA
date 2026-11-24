from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from core.errors import AppError
from schemas.health import HealthResponse
from services.health_service import HealthService
from db.database import database

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthService().get_status()


@router.get("/health/database")
def get_database_health() -> dict[str, str]:
    try:
        database.is_connected()
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError as exc:
        raise AppError(
            "Database is unavailable.",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="database_unavailable",
        ) from exc
