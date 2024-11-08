from typing import List
from collections import namedtuple


Clause = namedtuple("Clause", ["field", "operator", "value"])


class WhereFactory(object):

    def __init__(self, clauses: List[Clause]):
        self.__clauses = clauses
        self.__validate_clauses()
        self.__set_where()

    def __validate_clauses(self):
        for c in self.__clauses:
            if c.operator not in [">", "<", ">=", "<=", "="]:
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
