from config.settings import settings
from schemas.health import HealthResponse


class HealthService:
    def get_status(self) -> HealthResponse:
        return HealthResponse(
            status="ok",
            service=settings.app_name,
            version=settings.app_version,
            environment=settings.environment,
        )
