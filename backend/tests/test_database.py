from db.database import engine


def test_database_engine_is_configured_for_postgresql() -> None:
    assert engine.dialect.name == "postgresql"
