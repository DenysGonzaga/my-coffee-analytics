import duckdb
from datetime import datetime
from tabulate import tabulate
from collections import namedtuple
from typing import List
from dateutil.parser import parse

table_name = "tb_coffee_analytics"
conn = duckdb.connect("coffee_analytics.duckdb")

tables = [x[0] for x in conn.execute("SHOW TABLES").fetchall()]

if table_name not in tables:
    conn.execute("CREATE SEQUENCE seq_personid START 1 INCREMENT 1;")
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER DEFAULT nextval('seq_personid'),
            record_date TIMESTAMP,
            wter_quant SMALLINT,
            coff_quant SMALLINT,
            clic_quant SMALLINT,
            wtem_quant SMALLINT,
            color_score SMALLINT,
            flavor_score SMALLINT,
            smells_score SMALLINT
        )
        """
    )


Clause = namedtuple('Clause', ['field', 'operator', 'value'])

class WhereFactory(object):

    def __init__(self, clauses: List[Clause]):
        self.__clauses = clauses
        self.__validate_clauses()
        self.__set_where()

    def __validate_clauses(self):
        for c in self.__clauses:
            if c.operator not in ['>', '<', '>=', '<=', '=']:
                print(f"Err: Clause operator not found: '{c.operator}'")
                exit(-1)
    
    def __set_where(self):
        self.where = " WHERE "
        self.parameters = []

        for c in self.__clauses:
            self.where += f"{c.field} {c.operator} ? AND "
            self.parameters.append(c.value)

        self.where = self.where[:-5]



def make_question(message, validate_type, retry=1):
    user_input = input(message)

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
    wter = make_question("How much water did you used (gram)? ", int)
    coff = make_question("How much coffee did you used (gram)? ", int)
    clic = make_question("How many clicks did you make on your grinder?", int)
    wtem = make_question("What was the water temperature when you infused the coffee? ", int)

    dtn = datetime.now()
    dt_insert = datetime(dtn.year, dtn.month, dtn.day, dtn.hour, dtn.minute)

    conn.execute(
        f"""INSERT INTO {table_name} (record_date, 
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
            FROM {table_name}"""
    
    sql = sql if WhereFactory is None else sql + w_fact.where
    params = [] if WhereFactory is None else w_fact.parameters

    res = conn.execute(sql, params).fetchall()    
    print(tabulate(res, headers=["Record ID", "Record Data","Water Quantity (gr)", "Coffee Quantity (gr)", "Grinder Clicks", "Water Temperature (Celsius)"]))


#list_brew(WhereFactory([Clause('record_date', '>=', datetime(2024, 11, 7))]))

def main(show_menu=True):
    if show_menu:
        p_commands = [
            (1, 'Add a new brew data.'),
            (2, 'List all brews.'),
            (3, 'Filter an specific brew by day date.'),
            (4, 'Add feedback to a brew.'),
            (0, 'Exit program.')
        ]
        
        print(tabulate(p_commands, headers=["Key", "Operation Description"]))
    
    cmd = make_question("Operation: ", int)

    match cmd:
        case 0:
            print("Bye !")
            exit(0)
        case 1: 
            add_brew()
        case 2:
            list_brew()
        case 3:
            dt_begin = make_question("Date to filter: ", datetime)
            dt_end = datetime(dt_begin.year, dt_begin.month, dt_begin.day, 23, 59, 59)
            list_brew(WhereFactory([Clause('record_date', '>=', dt_begin), Clause('record_date', '<=', dt_end)]))
       

    main(False)
    
if __name__ == "__main__":
    main()