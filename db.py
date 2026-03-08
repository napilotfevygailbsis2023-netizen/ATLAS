import sqlite3, hashlib, os, secrets

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atlas.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            fname    TEXT NOT NULL,
            lname    TEXT NOT NULL,
            email    TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token   TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(fname, lname, email, password):
    try:
        conn = get_conn()
        conn.execute("INSERT INTO users (fname,lname,email,password) VALUES (?,?,?,?)",
                     (fname.strip(), lname.strip(), email.strip().lower(), hash_pw(password)))
        conn.commit()
        conn.close()
        return True, "Account created!"
    except sqlite3.IntegrityError:
        return False, "Email already registered."
    except Exception as e:
        return False, str(e)

def login_user(email, password):
    conn = get_conn()
    user = conn.execute("SELECT * FROM users WHERE email=? AND password=?",
                        (email.strip().lower(), hash_pw(password))).fetchone()
    conn.close()
    if user:
        token = secrets.token_hex(32)
        conn = get_conn()
        conn.execute("INSERT INTO sessions (token, user_id) VALUES (?,?)", (token, user["id"]))
        conn.commit()
        conn.close()
        return True, token, dict(user)
    return False, None, None

def get_user_by_token(token):
    if not token:
        return None
    try:
        conn = get_conn()
        row = conn.execute("""
            SELECT u.* FROM users u
            JOIN sessions s ON s.user_id = u.id
            WHERE s.token = ?
        """, (token,)).fetchone()
        conn.close()
        return dict(row) if row else None
    except:
        return None

def logout(token):
    try:
        conn = get_conn()
        conn.execute("DELETE FROM sessions WHERE token=?", (token,))
        conn.commit()
        conn.close()
    except:
        pass

init_db()
