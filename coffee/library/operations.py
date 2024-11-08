from datetime import datetime
from tabulate import tabulate
from dateutil.parser import parse

from coffee.library.config import settings
from coffee.library.database import DuckDbConnection
from coffee.library.model import Clause, WhereFactory


def make_question(message, validate_type, retry=1):
    user_input = input(f"{message} ")

    if validate_type == int:
        user_input = user_input.replace(" ", "")

        if user_input.isnumeric():
            return int(user_input)
        else:
            if retry == 3:
                print("Exceeded Retries, ending application.")
                exit(0)
            else:
                print("Value type incorrect. Try again.")
                make_question(message, validate_type, retry + 1)
    elif validate_type == datetime:
        try:
            return parse(user_input)
        except ValueError as ve:
            print("Unrecognized date format. Try again.")
            make_question(message, validate_type, retry + 1)


def add_brew():
    wter = make_question("How much water did you used (gram)?", int)
    coff = make_question("How much coffee did you used (gram)?", int)
    clic = make_question("How many clicks did you make on your grinder?", int)
    wtem = make_question(
        "What was the water temperature when you infused the coffee?", int
    )

    dtn = datetime.now()
    dt_insert = datetime(dtn.year, dtn.month, dtn.day, dtn.hour, dtn.minute)

    with DuckDbConnection() as conn:
        conn.execute(
            f"""INSERT INTO {settings.default.table_name} (record_date, 
                                        wter_quant, 
                                        coff_quant,
                                        clic_quant,
                                        wtem_quant) 
                        VALUES (?, ?, ?, ?, ?)""",
            (dt_insert, wter, coff, clic, wtem),
        )


def list_brew(w_fact: WhereFactory = None):
    sql = f"""SELECT id,
                record_date, 
                wter_quant,
                coff_quant, 
                clic_quant,
                wtem_quant 
            FROM {settings.default.table_name}"""

    sql = sql if w_fact is None else sql + w_fact.where
    params = [] if w_fact is None else w_fact.parameters

    with DuckDbConnection() as conn:
        res = conn.execute(sql, params).fetchall()
        print(
            tabulate(
                res,
                headers=[
                    "Record ID",
                    "Record Data",
                    "Water Quantity (gr)",
                    "Coffee Quantity (gr)",
                    "Grinder Clicks",
                    "Water Temperature (Celsius)",
                ],
            )
        )
