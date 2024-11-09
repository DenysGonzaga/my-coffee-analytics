"""
Testing module to coffeeanalytics.library.database.
"""
import pytest

from coffeeanalytics.library.config import settings
from coffeeanalytics.library.database import DuckDbConnection, init_database

from tests.custom_fixtures import temp_db

settings.setenv("tests")


@pytest.fixture(autouse=True)
def auto_fixture(temp_db):
    """
    Temp db autouse fixture
    """
    pass


def test_db_connection():
    """
    Testing db connection.
    """
    with DuckDbConnection() as conn:
        duck_data = conn.execute("SELECT 1").fetchall()

    assert len(duck_data) > 0


def test_init_database():
    """
    Testing database initialization and his states.
    """
    assert init_database() is True
    assert init_database() is False
