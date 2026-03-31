"""
ATLAS — MySQL Migration Script
Run ONCE before restarting your server:
    python db_migration.py

Adds photo_url column to users and tour_guides tables (MySQL version).
"""
from db_config import DB_CONFIG
import mysql.connector

conn = mysql.connector.connect(**DB_CONFIG)
cur  = conn.cursor()

def add_col(table, col, col_type="VARCHAR(500) DEFAULT ''"):
    try:
        cur.execute(f"ALTER TABLE `{table}` ADD COLUMN `{col}` {col_type}")
        conn.commit()
        print(f"  + Added '{col}' to '{table}'")
    except mysql.connector.Error as e:
        if e.errno == 1060:  # Duplicate column name
            print(f"  = '{col}' already in '{table}' (skipped)")
        else:
            print(f"  ! Error on '{table}'.'{col}': {e}")

print(f"Connected to MySQL database: {DB_CONFIG['database']}\n")

add_col("users",       "photo_url")
add_col("tour_guides", "photo_url")

cur.close()
conn.close()
print("\nDone — restart ATLAS server.")
