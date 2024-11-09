import sys
from datetime import datetime
from tabulate import tabulate

from coffeeanalytics.library.database import init_database
from coffeeanalytics.library.model import Clause, WhereFactory
from coffeeanalytics.library.operations import make_question, BrewOperations


def main(show_menu=True):
    if show_menu:
        p_commands = [
            (1, "Add a new brew data."),
            (2, "List all brews."),
            (3, "Filter an specific brew by day date."),
            (4, "Return last brew filtered by type."),
            (5, "Add feedback to a brew."),
            (0, "Exit program."),
        ]

        print(tabulate(p_commands, headers=["Key", "Operation Description"]))

    cmd = make_question("Operation:", int)

    match cmd:
        case 0:
            print("Bye ! See you soon !")
            sys.exit(0)
        case 1:
            BrewOperations.add_brew()
        case 2:
            BrewOperations.list_brew()
        case 3:
            dt_begin = make_question("Date to filter:", datetime)
            dt_end = datetime(dt_begin.year, dt_begin.month, dt_begin.day, 23, 59, 59)
            BrewOperations.list_brew(
                WhereFactory(
                    [
                        Clause("record_date", ">=", dt_begin),
                        Clause("record_date", "<=", dt_end),
                    ]
                )
            )
        case 4:
            brew_type = make_question("Brew Method:", str)
            BrewOperations.list_brew(
                WhereFactory([Clause("brew_type", "like", f"%{brew_type}%")])
            )
        case 5:
            brew_type = make_question("Input a brew id:", int)
            BrewOperations.add_brew_feedback(
                WhereFactory([Clause("brew_id", "=", brew_type)])
            )

    main(False)


if __name__ == "__main__":
    init_database()
    main()
