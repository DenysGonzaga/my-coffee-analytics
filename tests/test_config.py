"""
Testing module to coffeeanalytics.library.config.
"""
from coffeeanalytics.library.config import settings

settings.setenv("tests")


def test_configs():
    """
    Test if all necessary configs are being acessible.
    """
    assert "database_path" in settings
    assert "database_name" in settings
    assert "table_name" in settings
    assert "table_name" in settings
