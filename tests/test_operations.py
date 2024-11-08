import os
import pytest
from pathlib import Path
from coffee.library.config import settings

from coffee.library.database import *
from coffee.library.operations import *


@pytest.fixture(scope="module")
def temp_db():
    settings.set("database_name", settings.database_name + "test_operations")

    yield DuckDbConnection()

    db_path = Path(os.path.join(settings.database_path, f"{settings.database_name}"))

    if db_path.suffix != ".duckdb":
        db_path = str(db_path.with_suffix(".duckdb"))

    os.remove(db_path)


def test_make_question_int(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "20")
    output_data = make_question("tip something", int)
    assert isinstance(output_data, int)


def test_make_question_validate_datetime(monkeypatch):
    input_data = iter(["DDDD", "2020-10-01 01:20:23"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_data))
    assert make_question("tip something", datetime) == datetime(2020, 10, 1, 1, 20, 23)


def test_make_question_str(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "test")
    output_data = make_question("tip something", str)
    assert isinstance(output_data, str)


def test_make_question_retries(monkeypatch):
    input_data = iter(["40d", "30"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_data))
    output_data = make_question("tip something", int)
    assert isinstance(output_data, int)


def test_make_question_after_max_retries(monkeypatch):
    input_data = iter(["40d", "30e", "34r"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_data))
    with pytest.raises(Exception):
        make_question("tip something", int)


def test_add_n_list_brew(temp_db, monkeypatch):
    with temp_db as _:
        init_database()
        input_data = iter(["20", "20", "20", "20", "20"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_data))
        BrewOperations.add_brew()
        BrewOperations.list_brew()
