from typing import List
from collections import namedtuple


ValidationValue = namedtuple(
    "ValidationValue", ["new_value", "error_validation_message"]
)
Clause = namedtuple("Clause", ["field", "operator", "value"])


class WhereFactory(object):

    def __init__(self, clauses: List[Clause]):
        self.__clauses = clauses
        self.__validate_clauses()
        self.__set_where()

    def __validate_clauses(self):
        for c in self.__clauses:
            if c.operator.lower() not in [">", "<", ">=", "<=", "=", "like"]:
                raise NotImplementedError(
                    f"Err: Clause operator not found: '{c.operator}'"
                )

    def __set_where(self):
        self.where = " WHERE "
        self.parameters = []

        for c in self.__clauses:
            self.where += f"{c.field} {c.operator} ? AND "
            self.parameters.append(c.value)

        self.where = self.where[:-5]

    def __len__(self):
        return len(self.__clauses)


    def add_clause(self, Clause):
        self.__clauses.append(Clause)
        self.__validate_clauses()
        self.__set_where()
