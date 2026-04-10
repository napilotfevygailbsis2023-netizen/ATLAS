# ─────────────────────────────────────────────
#  ATLAS — MySQL Database Configuration
#  Edit these values to match your MySQL server
# ─────────────────────────────────────────────
import os

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "atlas_db"),
    "charset": "utf8mb4",
    "autocommit": False,
}
