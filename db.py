# db.py
import sqlite3
from datetime import datetime


# Initialize DB + table
def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            name TEXT,
            email TEXT,
            address TEXT,
            card_name TEXT,
            ebay_item_id TEXT
        )
    """)
    conn.commit()
    conn.close()


# Insert a new submission
def log_submission(name, email, address, card_name, ebay_item_id):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO submissions (timestamp, name, email, address, card_name, ebay_item_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, name, email, address, card_name, ebay_item_id))
    conn.commit()
    conn.close()
