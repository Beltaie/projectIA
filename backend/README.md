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

## PostgreSQL

Start Docker Desktop, then create the dedicated database and application role:

```powershell
docker compose up -d postgres
docker compose ps
```

The application connection uses `DATABASE_URL` from `.env`. The database container creates:

- Database: `smartcampus`
- Least-privilege application role: `smartcampus_app`
- Schema ownership and privileges limited to `smartcampus`

Check database connectivity at `http://localhost:8000/health/database`.

## Temporary session memory

The API stores user and assistant messages in PostgreSQL so the agent can reload
the recent conversation before answering a follow-up:

1. `POST /sessions` creates a session and returns its `session_id`.
2. `POST /sessions/{session_id}/messages` stores a message with `role` (`user`
   or `assistant`) and `content`.
3. `GET /sessions/{session_id}/messages` returns the retained messages in
   chronological order.

Memory expires after one hour without a new message by default. It is limited
to 20 messages per session, 4,000 characters per message, and 1,000 active
sessions. Older messages are removed first; expired sessions are removed on
requests and by a background cleanup task. The expiration, session count,
message count, and cleanup interval are configurable through the
`SESSION_MEMORY_*` environment variables in `.env`.

## Run

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`
