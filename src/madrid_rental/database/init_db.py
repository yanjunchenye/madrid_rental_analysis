from pathlib import Path #para localizar el archivo schema.sql
from sqlalchemy import text #para escribir en SQL
from madrid_rental.database.connection import get_engine

SCHEMA_PATH = Path(__file__).resolve().parents[3] / "sql" / "schema.sql"

def init_db():
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(schema_sql))
    print("tablas creadas")

if __name__ == "__main__":
    init_db()