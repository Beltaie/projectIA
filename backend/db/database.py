from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from config.settings import settings


engine: Engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Database:
    def is_connected(self) -> bool:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True

    def get_session(self) -> Generator[Session, None, None]:
        with SessionLocal() as session:
            yield session


database = Database()


def get_database_session() -> Generator[Session, None, None]:
    yield from database.get_session()


def check_database_connection() -> None:
    database.is_connected()


def initialize_database() -> None:
    from db.models import Base

    Base.metadata.create_all(bind=engine)


def close_database() -> None:
    engine.dispose()
