from datetime import datetime
from tabulate import tabulate

from coffee.library.database import init_database
from coffee.library.model import Clause, WhereFactory
from coffee.library.operations import make_question, add_brew, list_brew


def main(show_menu=True):
    if show_menu:
        p_commands = [
            (1, "Add a new brew data."),
            (2, "List all brews."),
            (3, "Filter an specific brew by day date."),
            (4, "Add feedback to a brew."),
            (0, "Exit program."),
        ]

        print(tabulate(p_commands, headers=["Key", "Operation Description"]))

    cmd = make_question("Operation:", int)

    match cmd:
        case 0:
            print("Bye !")
            exit(0)
        case 1:
            add_brew()
        case 2:
            list_brew()
        case 3:
            dt_begin = make_question("Date to filter:", datetime)
            dt_end = datetime(dt_begin.year, dt_begin.month, dt_begin.day, 23, 59, 59)
            list_brew(
                WhereFactory(
                    [
                        Clause("record_date", ">=", dt_begin),
                        Clause("record_date", "<=", dt_end),
                    ]
                )
            )

    main(False)


if __name__ == "__main__":
    init_database()
    main()
