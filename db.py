import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

# Load variables from .env if present
load_dotenv()


def get_engine() -> Engine:
    """Return a SQLAlchemy engine for the PostgreSQL database."""
    url = os.getenv("DATABASE_URL")
    if not url:
        user = os.getenv("PGUSER", "postgres")
        password = os.getenv("PGPASSWORD", "postgres")
        host = os.getenv("PGHOST", "localhost")
        port = os.getenv("PGPORT", "5432")
        dbname = os.getenv("PGDATABASE", "postgres")
        url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(url)


def execute_query(query: str, params: dict | None = None) -> list[dict]:
    """Execute a raw SQL query and return rows as list of dictionaries."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(query), params or {})
        rows = [dict(row) for row in result]
    return rows
