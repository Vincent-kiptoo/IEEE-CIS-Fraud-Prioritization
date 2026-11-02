from pathlib import Path

PROJECT_ROOT =  Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "raw"

DATABASE_DIR = PROJECT_ROOT / "database"

DB_PATH = DATABASE_DIR / "ieee_fraud.duckdb"

SQLALCHEMY_DATABASE_URL = f"duckdb:///{DB_PATH.as_posix()}"
