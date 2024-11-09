"""
Testing module to coffeeanalytics.library.model.
"""

from datetime import datetime

import pytest

from coffeeanalytics.library.model import WhereFactory, Clause


def test_where_factory():
    """
    Testing WhereFactory clauses.
    """
    wh = WhereFactory(
        [
            Clause("field1", ">", 123),
            Clause("field2", "<", "321"),
            Clause("field3", ">=", datetime(2020, 12, 12, 23, 59, 59)),
            Clause("field4", "<=", "ddd"),
            Clause("field5", "=", "fff"),
            Clause("field5", "like", "fff"),
        ]
    ).where

    assert len(wh) == 97


def test_where_factory_clause_not_implemented():
    """
    Testing WhereFactory clauses using a non implemented operation.
    """
    with pytest.raises(NotImplementedError):
        WhereFactory([Clause("field1", ">>>", 123)])


def test_add_clause():
    """
    Testing WhereFactory adding a new clause.
    """
    wh = WhereFactory([Clause("field1", ">", 123)])
    wh.add_clause(Clause("field2", "=", "test"))
    assert len(wh) == 2
