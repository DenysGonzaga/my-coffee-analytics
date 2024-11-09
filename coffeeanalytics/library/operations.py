"""
Module to provide operations in general, to handle database, to receive data 
from command line etc.
"""

from datetime import datetime

from tabulate import tabulate
from dateutil.parser import parse

from coffeeanalytics.library.config import settings
from coffeeanalytics.library.database import DuckDbConnection
from coffeeanalytics.library.model import (
    WhereFactory,
    ValidationValue,
    MaxRetriesExceptions,
)


def validate_input(value: str, validate_type: type):
    """
    Validate type of a input.

    Attributes
    ----------
    value (str): Value to be validated.
    validate_type (type): Desired type.
    """
    if validate_type == int:
        value = value.replace(" ", "")

        if value.isnumeric():
            return ValidationValue(int(value), None)
        return ValidationValue(None, "Wrong number format.")

    if validate_type == datetime:
        try:
            return ValidationValue(parse(value), None)
        except ValueError:
            return ValidationValue(None, "Wrong date format.")

    return ValidationValue(str(value), None)


def make_question(message: str, validate_type: type, retry: int=1, max_retries:int=3):
    """
    Function that retrives input from user.

    Attributes
    ----------
    message (str): Message question to be displayed.
    validate_type (type): Desired type.
    retry (int): Current retry value.
    max_retries (int): Max retry.
    """
    user_input = input(f"{message} ")

    if retry >= max_retries:
        raise MaxRetriesExceptions("Max retries exceeded.")

    validation: ValidationValue = validate_input(user_input, validate_type)

    if validation.error_validation_message is None:
        return validation.new_value

    print(validation.error_validation_message + ". Try again...")
    return make_question(message, validate_type, retry + 1)


class BrewOperations:
    """
    A class to handle brew operations.
    """

    @staticmethod
    def add_brew():
        """
        Add a new brew to database.
        """
        btyp = make_question(
            " - You used which method in your brew (e.g., French Press, Chemex etc) ?",
            str,
        )
        wter = make_question(" - How much water did you used (gram)?", int)
        coff = make_question(" - How much coffee did you used (gram)?", int)
        clic = make_question(" - How many clicks did you make on your grinder?", int)
        wtem = make_question(
            " - What was the water temperature when you infused the coffee?", int
        )

        dtn = datetime.now()
        dt_insert = datetime(dtn.year, dtn.month, dtn.day, dtn.hour, dtn.minute)

        with DuckDbConnection() as conn:
            conn.execute(
                f"""INSERT INTO {settings.table_name} (record_date,
                                            brew_type, 
                                            wter_quant, 
                                            coff_quant,
                                            clic_quant,
                                            wtem_quant) 
                            VALUES (?, ?, ?, ?, ?, ?)""",
                (dt_insert, btyp, wter, coff, clic, wtem),
            )

        print("Brew saved !")

    @staticmethod
    def add_brew_feedback(w_fact: WhereFactory):
        """
        Function to add a new brew feedback to an existing brew.

        Attributes
        ----------
        w_fact (WhereFactory): Where clause to find a brew to update.
        """
        print(
            "You're free to use your scale (e.g., 0 to 10 or 1 to 5), but, "
            + "just to have a fair comparison, use the same scale for all records."
        )
        c_score = make_question(" - Color Score:", int)
        f_score = make_question(" - Flavor Score:", int)
        s_score = make_question(" - Smells Score:", int)

        sql = f"""UPDATE {settings.table_name} SET color_score = ?,
                                                    flavor_score = ?,
                                                    smells_score = ?
                """

        sql = sql + w_fact.where
        params = [c_score, f_score, s_score] + w_fact.parameters

        with DuckDbConnection() as conn:
            conn.execute(sql, params)

    @staticmethod
    def list_brew(w_fact: WhereFactory = None):
        """
        Function to list brews.

        Attributes
        ----------
        w_fact (WhereFactory): Where clause to find list of brews.
        """
        sql = f"""SELECT brew_id,
                    CAST(record_date AS DATE) AS record_date, 
                    brew_type,
                    wter_quant,
                    coff_quant, 
                    clic_quant,
                    wtem_quant,
                    color_score,
                    flavor_score,
                    smells_score
                FROM {settings.table_name}"""

        sql = sql if w_fact is None else sql + w_fact.where
        params = [] if w_fact is None else w_fact.parameters

        with DuckDbConnection() as conn:
            res = conn.execute(sql, params).fetchall()
            print(
                tabulate(
                    res,
                    headers=[
                        "Brew ID",
                        "Date",
                        "Method",
                        "Water (gr)",
                        "Coffee (gr)",
                        "Grinder Clicks",
                        "Water Temp",
                        "Color Score",
                        "Flavor Score",
                        "Smells Score",
                    ],
                )
            )
