import sqlite3, hashlib, os, secrets
sys_path = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(sys_path, "atlas.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

def init_guide_tables():
    conn = get_conn()
    conn.execute("""CREATE TABLE IF NOT EXISTS tour_guides (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        fname       TEXT NOT NULL,
        lname       TEXT NOT NULL,
        email       TEXT UNIQUE NOT NULL,
        password    TEXT NOT NULL,
        phone       TEXT DEFAULT '',
        city        TEXT DEFAULT 'Manila',
        languages   TEXT DEFAULT 'EN, FIL',
        speciality  TEXT DEFAULT 'General Tours',
        bio         TEXT DEFAULT '',
        rate        TEXT DEFAULT 'P1,500/day',
        availability TEXT DEFAULT 'Mon-Sun',
        status      TEXT DEFAULT 'active',
        created     DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS guide_sessions (
        token       TEXT PRIMARY KEY,
        guide_id    INTEGER NOT NULL,
        created     DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS tour_packages (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        guide_id    INTEGER NOT NULL,
        title       TEXT NOT NULL,
        description TEXT DEFAULT '',
        price       TEXT NOT NULL,
        duration    TEXT DEFAULT 'Full Day',
        inclusions  TEXT DEFAULT '',
        city        TEXT DEFAULT 'Manila',
        status      TEXT DEFAULT 'active',
        created     DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS bookings (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        guide_id    INTEGER NOT NULL,
        tourist_name TEXT NOT NULL,
        tourist_email TEXT DEFAULT '',
        tourist_phone TEXT DEFAULT '',
        package_id  INTEGER,
        package_title TEXT DEFAULT '',
        tour_date   TEXT NOT NULL,
        pax         INTEGER DEFAULT 1,
        notes       TEXT DEFAULT '',
        status      TEXT DEFAULT 'pending',
        guide_notes TEXT DEFAULT '',
        created     DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS guide_ratings (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        guide_id    INTEGER NOT NULL,
        tourist_name TEXT NOT NULL,
        rating      INTEGER NOT NULL,
        feedback    TEXT DEFAULT '',
        created     DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()

# ── GUIDE AUTH ──
def register_guide(fname, lname, email, password, phone, city):
    try:
        conn = get_conn()
        conn.execute("INSERT INTO tour_guides (fname,lname,email,password,phone,city) VALUES (?,?,?,?,?,?)",
                     (fname.strip(), lname.strip(), email.strip().lower(), hash_pw(password), phone.strip(), city))
        conn.commit(); conn.close()
        return True, "Account created!"
    except sqlite3.IntegrityError:
        return False, "Email already registered."
    except Exception as e:
        return False, str(e)

def login_guide(email, password):
    conn = get_conn()
    guide = conn.execute("SELECT * FROM tour_guides WHERE email=? AND password=?",
                         (email.strip().lower(), hash_pw(password))).fetchone()
    conn.close()
    if not guide: return False, None, None
    token = secrets.token_hex(32)
    conn = get_conn()
    conn.execute("INSERT INTO guide_sessions (token,guide_id) VALUES (?,?)", (token, guide["id"]))
    conn.commit(); conn.close()
    return True, token, dict(guide)

def get_guide_by_token(token):
    if not token: return None
    try:
        conn = get_conn()
        row = conn.execute("""SELECT g.* FROM tour_guides g
            JOIN guide_sessions s ON s.guide_id=g.id WHERE s.token=?""", (token,)).fetchone()
        conn.close()
        return dict(row) if row else None
    except: return None

def logout_guide(token):
    try:
        conn = get_conn()
        conn.execute("DELETE FROM guide_sessions WHERE token=?", (token,))
        conn.commit(); conn.close()
    except: pass

def get_guide_by_id(gid):
    conn = get_conn()
    row = conn.execute("SELECT * FROM tour_guides WHERE id=?", (gid,)).fetchone()
    conn.close()
    return dict(row) if row else None

def update_guide_profile(gid, data):
    conn = get_conn()
    conn.execute("""UPDATE tour_guides SET fname=?,lname=?,phone=?,city=?,languages=?,
        speciality=?,bio=?,rate=?,availability=? WHERE id=?""",
        (data["fname"], data["lname"], data["phone"], data["city"], data["languages"],
         data["speciality"], data["bio"], data["rate"], data["availability"], gid))
    conn.commit(); conn.close()

def change_guide_password(gid, new_pw):
    conn = get_conn()
    conn.execute("UPDATE tour_guides SET password=? WHERE id=?", (hash_pw(new_pw), gid))
    conn.commit(); conn.close()

# ── PACKAGES ──
def get_packages(guide_id):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM tour_packages WHERE guide_id=? ORDER BY id DESC", (guide_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_package(guide_id, data):
    conn = get_conn()
    conn.execute("INSERT INTO tour_packages (guide_id,title,description,price,duration,inclusions,city) VALUES (?,?,?,?,?,?,?)",
                 (guide_id, data["title"], data.get("description",""), data["price"],
                  data.get("duration","Full Day"), data.get("inclusions",""), data.get("city","Manila")))
    conn.commit(); conn.close()

def delete_package(pkg_id, guide_id):
    conn = get_conn()
    conn.execute("DELETE FROM tour_packages WHERE id=? AND guide_id=?", (pkg_id, guide_id))
    conn.commit(); conn.close()

# ── BOOKINGS ──
def get_bookings(guide_id, status=None):
    conn = get_conn()
    if status:
        rows = conn.execute("SELECT * FROM bookings WHERE guide_id=? AND status=? ORDER BY tour_date ASC", (guide_id, status)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM bookings WHERE guide_id=? ORDER BY tour_date ASC", (guide_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_booking_status(booking_id, guide_id, status, notes=""):
    conn = get_conn()
    conn.execute("UPDATE bookings SET status=?, guide_notes=? WHERE id=? AND guide_id=?",
                 (status, notes, booking_id, guide_id))
    conn.commit(); conn.close()

def add_booking(data):
    conn = get_conn()
    conn.execute("""INSERT INTO bookings (guide_id,tourist_name,tourist_email,tourist_phone,
        package_id,package_title,tour_date,pax,notes) VALUES (?,?,?,?,?,?,?,?,?)""",
        (data["guide_id"], data["tourist_name"], data.get("tourist_email",""),
         data.get("tourist_phone",""), data.get("package_id",0), data.get("package_title",""),
         data["tour_date"], int(data.get("pax",1)), data.get("notes","")))
    conn.commit(); conn.close()

# ── RATINGS ──
def get_ratings(guide_id):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM guide_ratings WHERE guide_id=? ORDER BY created DESC", (guide_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_rating(guide_id, tourist_name, rating, feedback):
    conn = get_conn()
    conn.execute("INSERT INTO guide_ratings (guide_id,tourist_name,rating,feedback) VALUES (?,?,?,?)",
                 (guide_id, tourist_name, int(rating), feedback))
    conn.commit(); conn.close()

def get_avg_rating(guide_id):
    conn = get_conn()
    row = conn.execute("SELECT AVG(rating) as avg, COUNT(*) as cnt FROM guide_ratings WHERE guide_id=?", (guide_id,)).fetchone()
    conn.close()
    return round(row["avg"] or 0, 1), row["cnt"]

# ── PUBLIC GUIDE LISTING (for tourists) ──
def get_public_guides(city=None):
    conn = get_conn()
    if city and city != "All":
        rows = conn.execute("SELECT * FROM tour_guides WHERE status='active' AND city=? ORDER BY id DESC", (city,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM tour_guides WHERE status='active' ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

init_guide_tables()
