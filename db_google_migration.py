"""
ATLAS — Google OAuth Migration Script
Run ONCE before restarting your server:
    python db_google_migration.py

Adds google_id and photo_url columns to the users table so Google
sign-in can match returning users and store their profile picture.
"""
from db_config import DB_CONFIG
import mysql.connector

conn = mysql.connector.connect(**DB_CONFIG)
cur  = conn.cursor()

def add_col(table, col, col_type):
    try:
        cur.execute(f"ALTER TABLE `{table}` ADD COLUMN `{col}` {col_type}")
        conn.commit()
        print(f"  + Added '{col}' to '{table}'")
    except mysql.connector.Error as e:
        if e.errno == 1060:
            print(f"  = '{col}' already in '{table}' (skipped)")
        else:
            print(f"  ! Error on '{table}'.'{col}': {e}")

print(f"Connected to: {DB_CONFIG['database']}\n")

# google_id — stores the Google sub/uid so we can match returning users
add_col("users", "google_id",  "VARCHAR(128) DEFAULT NULL")

# photo_url — stores Google profile picture URL
add_col("users", "photo_url",  "VARCHAR(500) DEFAULT ''")

# Make password nullable so Google-only users don't need one
try:
    cur.execute("ALTER TABLE `users` MODIFY COLUMN `password` VARCHAR(255) DEFAULT NULL")
    conn.commit()
    print("  + Made 'password' column nullable for Google-only accounts")
except mysql.connector.Error as e:
    print(f"  = password column already nullable or error: {e}")

cur.close()
conn.close()
print("\nDone — restart ATLAS server.")
