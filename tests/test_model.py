import pytest
from datetime import datetime

from coffee.library.model import *
from coffee.library.config import settings


def test_where_factory():
    wh = WhereFactory(
        [
            Clause("field1", ">", 123),
            Clause("field2", "<", "321"),
            Clause("field3", ">=", datetime(2020, 12, 12, 23, 59, 59)),
            Clause("field4", "<=", "ddd"),
            Clause("field5", "=", "fff"),
        ]
    ).where

    assert len(wh) == 79


def test_where_factory_clause_not_implemented():
    with pytest.raises(NotImplementedError):
        WhereFactory([Clause("field1", ">>>", 123)])
