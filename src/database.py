
import duckdb

from pathlib import Path
from src.config import DB_PATH, DATA_DIR


def database_connection() -> duckdb.DuckDBPyConnection:
    """Establishes a connection to the persistent DuckDB database."""

    conn = duckdb.connect(str(DB_PATH))
    return conn


def create_csv_view(
    conn: duckdb.DuckDBPyConnection,
    view_name: str,
    csv_path: Path
) -> None:
    """Creates or replaces views from CSV files."""

    path_string = str(csv_path)
    safe_path = path_string.replace("'", "''")

    sql = f"""
        CREATE OR REPLACE VIEW {view_name} AS
        SELECT *
        FROM read_csv_auto(
            '{safe_path}',
            auto_detect = true
        );
    """

    conn.execute(sql)


def create_all_csv_views(conn: duckdb.DuckDBPyConnection) -> None:
    """Register all IEEE-CIS CSV files as persistent DuckDB views."""

    csv_files = {
        "train_transaction": DATA_DIR / "train_transaction.csv",
        "train_identity": DATA_DIR / "train_identity.csv",
        "test_transaction": DATA_DIR / "test_transaction.csv",
        "test_identity": DATA_DIR / "test_identity.csv",
        "sample_submission": DATA_DIR / "sample_submission.csv",
    }

    for view_name, csv_path in csv_files.items():
        create_csv_view(conn, view_name, csv_path)
        print(f"Successfully registered view: {view_name}")
