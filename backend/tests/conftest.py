"""Shared fixtures for the chat-session tests.

These tests need a REAL PostgreSQL database: the models use gen_random_uuid(),
TIMESTAMPTZ and ON DELETE CASCADE, none of which SQLite reproduces.

Default target: the throwaway database from compose.local-test.yml (port 5433).
Override with the TEST_DATABASE_URL environment variable.

WARNING: every test that uses the `db` or `client` fixture empties
chat_sessions and chat_messages (TRUNCATE) before it runs.
"""

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from config.settings import settings
from database import get_db
from main import app

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://smartcampus:smartcampus_dev_password@localhost:5433/smartcampus",
)


@pytest.fixture(scope="session")
def engine():
    if TEST_DATABASE_URL == settings.database_url:
        pytest.exit(
            "TEST_DATABASE_URL is the same as DATABASE_URL: refusing to TRUNCATE "
            "your development data. Point TEST_DATABASE_URL at the test database.",
            returncode=2,
        )
    test_engine = create_engine(
        TEST_DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 1} if "postgresql" in TEST_DATABASE_URL else {},
    )
    is_sqlite = False
    try:
        with test_engine.connect() as conn:
            conn.execute(text("SELECT 1 FROM chat_sessions LIMIT 1"))
    except OperationalError:
        from sqlalchemy import event
        from sqlalchemy.pool import StaticPool
        from database import Base
        is_sqlite = True
        test_engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        @event.listens_for(test_engine, "connect")
        def _set_sqlite_pragma(dbapi_conn, _conn_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        Base.metadata.create_all(bind=test_engine)

    test_engine._is_sqlite_fallback = is_sqlite
    yield test_engine
    test_engine.dispose()


@pytest.fixture
def session_factory(engine):
    if getattr(engine, "_is_sqlite_fallback", False):
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM chat_messages"))
            conn.execute(text("DELETE FROM chat_sessions"))
    else:
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE chat_sessions CASCADE"))
    return sessionmaker(bind=engine, autoflush=False)


@pytest.fixture
def db(session_factory):
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(session_factory):
    def override_get_db():
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
