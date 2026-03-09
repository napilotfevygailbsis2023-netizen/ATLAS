import sqlite3, hashlib, os, secrets

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atlas.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_admin():
    conn = get_conn()
    # admin accounts table
    conn.execute("""CREATE TABLE IF NOT EXISTS admins (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created  DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    # admin sessions
    conn.execute("""CREATE TABLE IF NOT EXISTS admin_sessions (
        token   TEXT PRIMARY KEY,
        admin_id INTEGER NOT NULL,
        created DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    # custom spots table for admin CRUD
    conn.execute("""CREATE TABLE IF NOT EXISTS custom_spots (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT NOT NULL,
        city     TEXT NOT NULL,
        category TEXT NOT NULL,
        type     TEXT NOT NULL,
        rating   REAL DEFAULT 4.0,
        entry    TEXT DEFAULT 'Free',
        hours    TEXT DEFAULT '8AM-5PM',
        desc     TEXT DEFAULT '',
        created  DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    # custom restaurants table
    conn.execute("""CREATE TABLE IF NOT EXISTS custom_restaurants (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT NOT NULL,
        city     TEXT NOT NULL,
        cuisine  TEXT NOT NULL,
        price    TEXT DEFAULT 'PHP 200-400',
        rating   REAL DEFAULT 4.0,
        hours    TEXT DEFAULT '10AM-10PM',
        created  DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    # page visit counter
    conn.execute("""CREATE TABLE IF NOT EXISTS visits (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        page    TEXT NOT NULL,
        visited DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    # user status column
    try:
        conn.execute("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active'")
    except: pass
    conn.commit()
    # seed default admin
    try:
        pw = hashlib.sha256("admin123".encode()).hexdigest()
        conn.execute("INSERT INTO admins (username, password) VALUES (?,?)", ("admin", pw))
        conn.commit()
    except: pass
    conn.close()

def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()

def admin_login(username, password):
    conn = get_conn()
    row = conn.execute("SELECT * FROM admins WHERE username=? AND password=?",
                       (username.strip(), hash_pw(password))).fetchone()
    conn.close()
    if row:
        token = secrets.token_hex(32)
        conn = get_conn()
        conn.execute("INSERT INTO admin_sessions (token, admin_id) VALUES (?,?)", (token, row["id"]))
        conn.commit(); conn.close()
        return token
    return None

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

# ── STATS ──
def get_stats():
    conn = get_conn()
    total_users   = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    active_users  = conn.execute("SELECT COUNT(*) FROM users WHERE status='active' OR status IS NULL").fetchone()[0]
    suspended     = conn.execute("SELECT COUNT(*) FROM users WHERE status='suspended'").fetchone()[0]
    total_spots   = conn.execute("SELECT COUNT(*) FROM custom_spots").fetchone()[0]
    total_rests   = conn.execute("SELECT COUNT(*) FROM custom_restaurants").fetchone()[0]
    total_visits  = conn.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
    conn.close()
    return {"total_users":total_users,"active_users":active_users,"suspended":suspended,
            "total_spots":total_spots,"total_rests":total_rests,"total_visits":total_visits}

# ── USERS ──
def get_all_users():
    conn = get_conn()
    rows = conn.execute("SELECT id,fname,lname,email,created,status FROM users ORDER BY created DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def set_user_status(uid, status):
    conn = get_conn()
    conn.execute("UPDATE users SET status=? WHERE id=?", (status, uid))
    conn.commit(); conn.close()

def delete_user(uid):
    conn = get_conn()
    conn.execute("DELETE FROM sessions WHERE user_id=?", (uid,))
    conn.execute("DELETE FROM users WHERE id=?", (uid,))
    conn.commit(); conn.close()

# ── SPOTS CRUD ──
def get_spots():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM custom_spots ORDER BY created DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_spot(name, city, category, stype, rating, entry, hours, desc):
    conn = get_conn()
    conn.execute("INSERT INTO custom_spots (name,city,category,type,rating,entry,hours,desc) VALUES (?,?,?,?,?,?,?,?)",
                 (name,city,category,stype,float(rating),entry,hours,desc))
    conn.commit(); conn.close()

def delete_spot(sid):
    conn = get_conn()
    conn.execute("DELETE FROM custom_spots WHERE id=?", (sid,))
    conn.commit(); conn.close()

# ── RESTAURANTS CRUD ──
def get_restaurants():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM custom_restaurants ORDER BY created DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_restaurant(name, city, cuisine, price, rating, hours):
    conn = get_conn()
    conn.execute("INSERT INTO custom_restaurants (name,city,cuisine,price,rating,hours) VALUES (?,?,?,?,?,?)",
                 (name,city,cuisine,price,float(rating),hours))
    conn.commit(); conn.close()

def delete_restaurant(rid):
    conn = get_conn()
    conn.execute("DELETE FROM custom_restaurants WHERE id=?", (rid,))
    conn.commit(); conn.close()

# ── VISIT TRACKING ──
def log_visit(page):
    try:
        conn = get_conn()
        conn.execute("INSERT INTO visits (page) VALUES (?)", (page,))
        conn.commit(); conn.close()
    except: pass

def get_visit_stats():
    conn = get_conn()
    rows = conn.execute("SELECT page, COUNT(*) as cnt FROM visits GROUP BY page ORDER BY cnt DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

init_admin()
