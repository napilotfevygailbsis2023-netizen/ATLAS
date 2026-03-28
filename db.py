import sqlite3, hashlib, os, secrets

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atlas.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=10)
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
            status   TEXT DEFAULT 'active',
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS admin_sessions (
            token      TEXT PRIMARY KEY,
            admin_id   INTEGER NOT NULL,
            created    DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS spots (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            city    TEXT NOT NULL,
            cat     TEXT NOT NULL,
            rating  REAL DEFAULT 4.5,
            entry   TEXT DEFAULT 'Free',
            hours   TEXT DEFAULT '8AM-6PM',
            desc    TEXT,
            visits  TEXT DEFAULT 'N/A'
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            city    TEXT NOT NULL,
            type    TEXT NOT NULL,
            price   TEXT DEFAULT 'Check restaurant',
            rating  REAL DEFAULT 4.0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pending_users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            fname    TEXT NOT NULL,
            lname    TEXT NOT NULL,
            email    TEXT NOT NULL,
            password TEXT NOT NULL,
            token    TEXT UNIQUE NOT NULL,
            created  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Seed default admin if none exists
    existing = conn.execute("SELECT COUNT(*) FROM admins").fetchone()[0]
    if existing == 0:
        conn.execute("INSERT INTO admins (username, password) VALUES (?,?)",
                     ("admin", hash_pw("atlas2026")))
    conn.commit()
    conn.close()

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

def store_pending_user(fname, lname, email, password):
    """Store unverified user and return verification token."""
    import secrets as _sec
    token = _sec.token_urlsafe(32)
    conn = get_conn()
    try:
        # Remove any old pending entry for this email
        conn.execute("DELETE FROM pending_users WHERE email=?", (email.strip().lower(),))
        conn.execute(
            "INSERT INTO pending_users (fname,lname,email,password,token) VALUES (?,?,?,?,?)",
            (fname.strip(), lname.strip(), email.strip().lower(), hash_pw(password), token)
        )
        conn.commit()
        return token
    except Exception as e:
        return None
    finally:
        conn.close()

def activate_user(token):
    """Move pending user to users table on email click."""
    conn = get_conn()
    try:
        row = conn.execute("SELECT * FROM pending_users WHERE token=?", (token,)).fetchone()
        if not row:
            return False, "Invalid or expired verification link."
        # Check email not already registered
        existing = conn.execute("SELECT id FROM users WHERE email=?", (row["email"],)).fetchone()
        if existing:
            conn.execute("DELETE FROM pending_users WHERE token=?", (token,))
            conn.commit()
            return False, "Email already registered. Please log in."
        conn.execute(
            "INSERT INTO users (fname,lname,email,password) VALUES (?,?,?,?)",
            (row["fname"], row["lname"], row["email"], row["password"])
        )
        conn.execute("DELETE FROM pending_users WHERE token=?", (token,))
        conn.commit()
        return True, "Account verified! You can now log in."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def email_already_registered(email):
    conn = get_conn()
    try:
        row = conn.execute("SELECT id FROM users WHERE email=?", (email.strip().lower(),)).fetchone()
        return row is not None
    finally:
        conn.close()

def register_user(fname, lname, email, password):
    try:
        conn = get_conn()
        conn.execute("INSERT INTO users (fname,lname,email,password) VALUES (?,?,?,?)",
                     (fname.strip(), lname.strip(), email.strip().lower(), hash_pw(password)))
        conn.commit(); conn.close()
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
    if not user:
        return False, None, None
    if dict(user).get("status","active") == "suspended":
        return "suspended", None, None
    token = secrets.token_hex(32)
    conn = get_conn()
    conn.execute("INSERT INTO sessions (token,user_id) VALUES (?,?)", (token, user["id"]))
    conn.commit(); conn.close()
    return True, token, dict(user)

def get_user_by_token(token):
    if not token: return None
    try:
        conn = get_conn()
        row = conn.execute("""SELECT u.* FROM users u
            JOIN sessions s ON s.user_id=u.id WHERE s.token=?""", (token,)).fetchone()
        conn.close()
        return dict(row) if row else None
    except: return None

def logout(token):
    try:
        conn = get_conn()
        conn.execute("DELETE FROM sessions WHERE token=?", (token,))
        conn.commit(); conn.close()
    except: pass

# ── ADMIN AUTH ──
def admin_login(username, password):
    conn = get_conn()
    admin = conn.execute("SELECT * FROM admins WHERE username=? AND password=?",
                         (username.strip(), hash_pw(password))).fetchone()
    conn.close()
    if admin:
        token = secrets.token_hex(32)
        conn = get_conn()
        conn.execute("INSERT INTO admin_sessions (token,admin_id) VALUES (?,?)", (token, admin["id"]))
        conn.commit(); conn.close()
        return True, token
    return False, None

def get_admin_by_token(token):
    if not token: return None
    try:
        conn = get_conn()
        row = conn.execute("""SELECT a.* FROM admins a
            JOIN admin_sessions s ON s.admin_id=a.id WHERE s.token=?""", (token,)).fetchone()
        conn.close()
        return dict(row) if row else None
    except: return None

def admin_logout(token):
    try:
        conn = get_conn()
        conn.execute("DELETE FROM admin_sessions WHERE token=?", (token,))
        conn.commit(); conn.close()
    except: pass

# ── USER MANAGEMENT ──
def get_all_users():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM users ORDER BY created DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def suspend_user(uid):
    conn = get_conn()
    conn.execute("UPDATE users SET status='suspended' WHERE id=?", (uid,))
    conn.commit(); conn.close()

def unsuspend_user(uid):
    conn = get_conn()
    conn.execute("UPDATE users SET status='active' WHERE id=?", (uid,))
    conn.commit(); conn.close()

def delete_user(uid):
    conn = get_conn()
    conn.execute("DELETE FROM sessions WHERE user_id=?", (uid,))
    conn.execute("DELETE FROM users WHERE id=?", (uid,))
    conn.commit(); conn.close()

# ── STATS ──
def get_stats():
    conn = get_conn()
    total_users    = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    active_users   = conn.execute("SELECT COUNT(*) FROM users WHERE status='active'").fetchone()[0]
    suspended      = conn.execute("SELECT COUNT(*) FROM users WHERE status='suspended'").fetchone()[0]
    total_spots    = conn.execute("SELECT COUNT(*) FROM spots").fetchone()[0]
    total_rests    = conn.execute("SELECT COUNT(*) FROM restaurants").fetchone()[0]
    conn.close()
    return {"total_users":total_users,"active_users":active_users,
            "suspended":suspended,"total_spots":total_spots,"total_rests":total_rests}

# ── SPOTS CRUD ──
def get_all_spots():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM spots ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_spot(data):
    conn = get_conn()
    conn.execute("INSERT INTO spots (name,city,cat,rating,entry,hours,desc) VALUES (?,?,?,?,?,?,?)",
                 (data["name"],data["city"],data["cat"],float(data.get("rating",4.5)),
                  data.get("entry","Free"),data.get("hours","8AM-6PM"),data.get("desc","")))
    conn.commit(); conn.close()

def delete_spot(sid):
    conn = get_conn()
    conn.execute("DELETE FROM spots WHERE id=?", (sid,))
    conn.commit(); conn.close()

# ── RESTAURANTS CRUD ──
def get_all_restaurants():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM restaurants ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_restaurant(data):
    conn = get_conn()
    conn.execute("INSERT INTO restaurants (name,city,type,price,rating) VALUES (?,?,?,?,?)",
                 (data["name"],data["city"],data["type"],
                  data.get("price","Check restaurant"),float(data.get("rating",4.0))))
    conn.commit(); conn.close()

def delete_restaurant(rid):
    conn = get_conn()
    conn.execute("DELETE FROM restaurants WHERE id=?", (rid,))
    conn.commit(); conn.close()

init_db()
