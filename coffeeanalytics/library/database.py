from os import path
from pathlib import Path

import duckdb

from coffeeanalytics.library.config import settings


class DuckDbConnection:

    def __init__(self):
        self.conn = None
        db_path = Path(path.join(settings.database_path, f"{settings.database_name}"))

        if db_path.suffix != ".duckdb":
            db_path = str(db_path.with_suffix(".duckdb"))

        self.db_path = db_path

    def __enter__(self):
        self.conn = duckdb.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.conn.close()


def init_database():
    with DuckDbConnection() as db:
        tables = [x[0] for x in db.execute("SHOW TABLES").fetchall()]

        if settings.table_name not in tables:
            db.execute("CREATE SEQUENCE seq_personid START 1 INCREMENT 1;")
            db.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {settings.table_name} (
                    brew_id INTEGER DEFAULT nextval('seq_personid'),
                    record_date TIMESTAMP,
                    brew_type VARCHAR,
                    wter_quant SMALLINT,
                    coff_quant SMALLINT,
                    clic_quant SMALLINT,
                    wtem_quant SMALLINT,
                    color_score SMALLINT DEFAULT 0,
                    flavor_score SMALLINT DEFAULT 0,
                    smells_score SMALLINT DEFAULT 0
                )
                """
            )

            return True
    return False
