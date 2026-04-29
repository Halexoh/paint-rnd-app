import sqlite3
from pathlib import Path

DB_PATH = Path("data/formulations.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS formulations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT NOT NULL,
        product_type TEXT NOT NULL,
        version TEXT NOT NULL,
        author TEXT,
        notes TEXT,
        measured_viscosity REAL,
        measured_ph REAL,
        measured_density REAL,
        measured_solids REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        formulation_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        material_name TEXT NOT NULL,
        amount REAL,
        unit TEXT,
        position INTEGER,
        solids_pct REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (formulation_id) REFERENCES formulations(id)
    )
    """)

    conn.commit()
    conn.close()