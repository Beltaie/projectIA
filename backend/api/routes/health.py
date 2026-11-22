from fastapi import APIRouter

from schemas.health import HealthResponse
from services.health_service import HealthService

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthService().get_status()
