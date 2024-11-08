import duckdb
from os import path
from pathlib import Path

from coffee.library.config import settings


class DuckDbConnection(object):

    def __enter__(self):
        db_path = Path(
            path.join(
                settings.default.database_path, f"{settings.default.database_name}"
            )
        )

        if db_path.suffix != ".duckdb":
            db_path = db_path.with_suffix(".duckdb")

        self.conn = duckdb.connect(str(db_path))
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.conn.close()


def init_database():
    with DuckDbConnection() as db:
        tables = [x[0] for x in db.execute("SHOW TABLES").fetchall()]

        if settings.default.table_name not in tables:
            db.execute("CREATE SEQUENCE seq_personid START 1 INCREMENT 1;")
            db.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {settings.default.table_name} (
                    brew_id INTEGER DEFAULT nextval('seq_personid'),
                    record_date TIMESTAMP,
                    brew_type VARCHAR,
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
