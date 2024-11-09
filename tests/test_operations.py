"""
Testing module to coffeeanalytics.library.operations.
"""

from datetime import datetime

import pytest

from coffeeanalytics.library.model import WhereFactory, Clause, MaxRetriesExceptions
from coffeeanalytics.library.database import init_database
from coffeeanalytics.library.operations import (
    validate_input,
    make_question,
    BrewOperations,
)

from tests.custom_fixtures import temp_db


@pytest.fixture(autouse=True)
def auto_fixture(temp_db):
    """
    Temp db autouse fixture
    """
    pass


@pytest.mark.parametrize("value", ["10", "4", "45"])
def test_validation_int(value):
    """
    Testing validation values with int type.
    """
    val = validate_input(value, int).new_value
    assert isinstance(val, int)
    assert val == int(value)


@pytest.mark.parametrize(
    "dt_fmt,value",
    [
        ("%Y-%m-%d %H:%M:%S", "2017-01-02 01:20:23"),
        ("%Y-%m-%d", "1988-12-20"),
        ("%Y/%m/%d", "1987/12/19"),
        ("%Y/%m/%d %H:%M:%S", "2012/10/29 19:20:59"),
    ],
)
def test_validation_datetime(dt_fmt, value):
    """
   Testing validation values with datetime type.
    """
    val = validate_input(value, datetime).new_value
    assert isinstance(val, datetime)
    assert val == datetime.strptime(value, dt_fmt)


def test_validation_error_int():
    """
    Testing validation values with int type and returning error.
    """
    evm = validate_input("INTEGER", int).error_validation_message
    assert len(evm) > 0
    assert evm == "Wrong number format."


def test_validation_error_datetime():
    """
    Testing validation values with datetime type and returning error.
    """
    evm = validate_input("DATE", datetime).error_validation_message
    assert len(evm) > 0
    assert evm == "Wrong date format."


def test_make_question_str(monkeypatch):
    """
    Testing how app handles a question input.
    """
    monkeypatch.setattr("builtins.input", lambda _: "test")
    output_data = make_question("tip something", str)
    assert isinstance(output_data, str)


def test_make_question_retries(monkeypatch):
    """
    Testing how app handles a question input with retry.
    """
    input_data = iter(["40d", "30"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_data))
    output_data = make_question("tip something", int)
    assert isinstance(output_data, int)


def test_make_question_after_max_retries(monkeypatch):
    """
    Testing how app handles a question input with retry and raising a exception
    due by max excedded Exception.
    """
    input_data = iter(["40d", "30e", "34r"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_data))
    with pytest.raises(MaxRetriesExceptions):
        make_question("tip something", int)


def test_add_n_list_brew(temp_db, monkeypatch):
    """
    Testing creating a new brew.
    """
    with temp_db as _:
        init_database()
        input_data = iter(["20", "20", "20", "20", "20"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_data))
        BrewOperations.add_brew()
        BrewOperations.list_brew()


def test_add_n_list_with_filter_brew(temp_db, monkeypatch):
    """
    Testing creating a new brew and listing.
    """
    with temp_db as _:
        init_database()
        input_data = iter(["20", "20", "20", "20", "20"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_data))
        BrewOperations.add_brew()
        BrewOperations.list_brew(WhereFactory([Clause("brew_id", "=", 1)]))


def test_add_feedback_brew(temp_db, monkeypatch):
    """
    Testing adding a feedback to already existed brew.
    """
    with temp_db as _:
        init_database()
        input_data = iter(["20", "20", "20", "20", "20", "5", "6", "4"])
        monkeypatch.setattr("builtins.input", lambda _: next(input_data))
        BrewOperations.add_brew()
        BrewOperations.add_brew_feedback(WhereFactory([Clause("brew_id", "=", 1)]))
