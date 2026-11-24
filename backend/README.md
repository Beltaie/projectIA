# SmartCampus AI Backend

FastAPI backend foundation for the SmartCampus AI platform.

## Structure

- `api/` - HTTP routers and route handlers
- `services/` - application and business logic
- `schemas/` - request and response models
- `config/` - environment-based configuration
- `core/` - middleware and shared error handling
- `tests/` - automated tests

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` to override local settings.

## Run

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`
