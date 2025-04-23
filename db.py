import psycopg2
import os

# Load from Railway connection string
DATABASE_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql://postgres:UptXxbjWSJNrUCBdmaCYEaaiqPgHHQDo@yamabiko.proxy.rlwy.net:16755/railway"
)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()


def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            address TEXT,
            card_name TEXT,
            ebay_item_id TEXT,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def log_submission(name, email, address, card_name, ebay_item_id):
    cursor.execute(
        "INSERT INTO orders (name, email, address, card_name, ebay_item_id) VALUES (%s, %s, %s, %s, %s)",
        (name, email, address, card_name, ebay_item_id)
    )
    conn.commit()
