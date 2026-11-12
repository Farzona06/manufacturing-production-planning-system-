import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("manufacturing.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sku TEXT NOT NULL UNIQUE,
        unit_price REAL NOT NULL DEFAULT 0 CHECK(unit_price >= 0),
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS raw_materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        unit TEXT NOT NULL,
        quantity REAL NOT NULL DEFAULT 0 CHECK(quantity >= 0),
        min_quantity REAL NOT NULL DEFAULT 0 CHECK(min_quantity >= 0)
    );
    CREATE TABLE IF NOT EXISTS production_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        plan_date TEXT NOT NULL,
        planned_quantity INTEGER NOT NULL CHECK(planned_quantity > 0),
        completed_quantity INTEGER NOT NULL DEFAULT 0 CHECK(completed_quantity >= 0),
        status TEXT NOT NULL DEFAULT 'Planned',
        FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE RESTRICT
    );
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        status TEXT NOT NULL DEFAULT 'New',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE RESTRICT
    );
    """)
    if db.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        db.executemany("INSERT INTO products(name, sku, unit_price) VALUES(?,?,?)", [
            ("Paxta mato", "MAT-001", 42000),
            ("Tayyor futbolka", "KIM-002", 65000),
            ("Ishchi kiyim", "KIM-003", 120000)
        ])
        db.executemany("INSERT INTO raw_materials(name, unit, quantity, min_quantity) VALUES(?,?,?,?)", [
            ("Paxta ipi", "kg", 250, 50),
            ("Bo‘yoq", "litr", 35, 40),
            ("Tugma", "dona", 1200, 200)
        ])
        db.commit()
    db.close()
