from datetime import datetime
from tabulate import tabulate

from coffee.library.database import init_database
from coffee.library.model import Clause, WhereFactory
from coffee.library.operations import make_question, BrewOperations


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
            exit(0)
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
            pass
        case 5:
            pass
            # brew_id = make_question("Brew ID:", int)
            # BrewOperations.add_brew_feedback(brew_id)

    main(False)


if __name__ == "__main__":
    try:
        init_database()
        main()
    except Exception as e:
        print(f"Application can't continue due an error: {str(e)}")
