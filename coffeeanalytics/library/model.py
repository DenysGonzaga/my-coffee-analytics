"""
Module to provide model classes.
"""

from typing import List
from collections import namedtuple


ValidationValue = namedtuple(
    "ValidationValue", ["new_value", "error_validation_message"]
)
Clause = namedtuple("Clause", ["field", "operator", "value"])


class WhereFactory:
    """
    A class to create WHERE clauses on the database queries.

    Attributes
    ----------
    clauses : List[Clause]
        List of Clauses to build where statement
    """

    def __init__(self, clauses: List[Clause]):
        self.__clauses = clauses
        self.__validate_clauses()
        self.__set_where()

    def __validate_clauses(self):
        """
        Internal function to validate clause operations.
        Allowed operations are ">", "<", ">=", "<=", "=", "like".
        """
        for c in self.__clauses:
            if c.operator.lower() not in [">", "<", ">=", "<=", "=", "like"]:
                raise NotImplementedError(
                    f"Err: Clause operator not found: '{c.operator}'"
                )

    def __set_where(self):
        """
        Internal function to build string where clause.
        """
        self.where = " WHERE "
        self.parameters = []

        for c in self.__clauses:
            self.where += f"{c.field} {c.operator} ? AND "
            self.parameters.append(c.value)

        self.where = self.where[:-5]

    def __len__(self):
        """
        Returning len of clauses.
        """
        return len(self.__clauses)

    def add_clause(self, clause: Clause):
        """
        Add a new clause to the list of clauses.

        Attributes
        ----------
        clause (Clause): A new clause to be added.
        """
        self.__clauses.append(clause)
        self.__validate_clauses()
        self.__set_where()


class MaxRetriesExceptions(Exception):
    """
    Exception raised for max retries on input data capture.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
