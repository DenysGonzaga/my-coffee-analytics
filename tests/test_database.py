import os
import pytest

from coffee.library.config import settings
from coffee.library.database import *

settings.setenv("tests")


@pytest.fixture(autouse=True, scope="module")
def temp_db():
    settings.set("database_name", settings.database_name + "test_database")

    yield DuckDbConnection()

    db_path = Path(path.join(settings.database_path, f"{settings.database_name}"))

    if db_path.suffix != ".duckdb":
        db_path = str(db_path.with_suffix(".duckdb"))

    os.remove(db_path)


def test_db_connection():
    with DuckDbConnection() as conn:
        duck_data = conn.execute("SELECT 1").fetchall()

    assert len(duck_data) > 0


def test_init_database():
    assert init_database() == True
    assert init_database() == False
