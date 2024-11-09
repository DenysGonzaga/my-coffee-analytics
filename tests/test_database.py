import os
from pathlib import Path

import pytest

from coffeeanalytics.library.config import settings
from coffeeanalytics.library.database import DuckDbConnection, init_database

settings.setenv("tests")


@pytest.fixture(autouse=True, scope="module")
def temp_db():
    settings.set("database_name", settings.database_name + "test_database")

    yield DuckDbConnection()

    db_path = Path(os.path.join(settings.database_path, f"{settings.database_name}"))

    if db_path.suffix != ".duckdb":
        db_path = str(db_path.with_suffix(".duckdb"))

    os.remove(db_path)


def test_db_connection():
    with DuckDbConnection() as conn:
        duck_data = conn.execute("SELECT 1").fetchall()

    assert len(duck_data) > 0


def test_init_database():
    assert init_database() is True
    assert init_database() is False
