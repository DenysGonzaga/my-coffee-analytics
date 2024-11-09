"""
Support module to store fixtures.
"""
import os
from pathlib import Path

import pytest
from coffeeanalytics.library.config import settings
from coffeeanalytics.library.database import DuckDbConnection

@pytest.fixture(autouse=True, scope="module")
def temp_db():
    """
    Fixture to generate a temporary database.
    """
    settings.set("database_name", settings.database_name + "test_database")

    yield DuckDbConnection()

    db_path = Path(os.path.join(settings.database_path, f"{settings.database_name}"))

    if db_path.suffix != ".duckdb":
        db_path = str(db_path.with_suffix(".duckdb"))

    os.remove(db_path)