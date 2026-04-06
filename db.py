import hashlib, secrets
try:
    import bcrypt
except ImportError:
    raise ImportError("bcrypt is not installed. Run: pip install bcrypt")
try:
    import mysql.connector
    from mysql.connector import IntegrityError
except ImportError:
    raise ImportError("mysql-connector-python is not installed. Run: pip install mysql-connector-python")

from db_config import DB_CONFIG

def get_conn():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def _cursor(conn):
    """Return a dict cursor."""
    return conn.cursor(dictionary=True)

def hash_pw(p):
    """Hash a password with bcrypt (salted). Returns a str for DB storage."""
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def check_pw(plain, hashed):
    """Verify a plain password against a bcrypt or legacy SHA-256 hash."""
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        # Legacy SHA-256 fallback — allows existing accounts to still log in
        return hashlib.sha256(plain.encode()).hexdigest() == hashed

# ── INIT ──
def init_db():
    conn = get_conn()
    cur  = _cursor(conn)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            fname       VARCHAR(100) NOT NULL,
            lname       VARCHAR(100) NOT NULL,
            email       VARCHAR(255) UNIQUE NOT NULL,
            password    VARCHAR(64)  NOT NULL,
            photo_url   VARCHAR(500) DEFAULT '',
            status      VARCHAR(20)  DEFAULT 'active',
            totp_secret VARCHAR(64)  DEFAULT '',
            totp_enabled TINYINT(1)  DEFAULT 0,
            created     DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    # Auto-migrate: add photo_url if missing (for existing databases)
    try:
        cur.execute("ALTER TABLE users ADD COLUMN photo_url VARCHAR(500) DEFAULT ''")
        conn.commit()
    except Exception:
        pass  # Column already exists
    for _col, _defn in [
        ("totp_secret",  "VARCHAR(64) DEFAULT ''"),
        ("totp_enabled", "TINYINT(1) DEFAULT 0"),
    ]:
        try:
            cur.execute(f"ALTER TABLE users ADD COLUMN {_col} {_defn}")
            conn.commit()
        except Exception:
            pass  # Column already exists

    cur.execute("""
        CREATE TABLE IF NOT EXISTS view_history (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            user_id    INT          NOT NULL,
            item_type  VARCHAR(20)  NOT NULL,
            item_name  VARCHAR(200) NOT NULL,
            item_city  VARCHAR(100) DEFAULT '',
            item_extra VARCHAR(300) DEFAULT '',
            viewed_at  DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS flight_bookings (
            id             INT AUTO_INCREMENT PRIMARY KEY,
            user_id        INT          NOT NULL,
            airline        VARCHAR(200) NOT NULL,
            origin         VARCHAR(200) NOT NULL,
            destination    VARCHAR(200) NOT NULL,
            dep_time       VARCHAR(20)  DEFAULT '',
            arr_time       VARCHAR(20)  DEFAULT '',
            flight_number  VARCHAR(50)  DEFAULT '',
            status         VARCHAR(50)  DEFAULT 'Scheduled',
            booked_at      DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token   VARCHAR(64) PRIMARY KEY,
            user_id INT         NOT NULL,
            created DATETIME    DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id        INT AUTO_INCREMENT PRIMARY KEY,
            username  VARCHAR(100) UNIQUE NOT NULL,
            password  VARCHAR(64)  NOT NULL,
            email     VARCHAR(255) DEFAULT 'admin@atlas.ph',
            fullname  VARCHAR(200) DEFAULT 'ATLAS Administrator',
            created   DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    # Auto-migrate: add missing admin columns for existing databases
    for _col, _defn in [
        ("email",    "VARCHAR(255) DEFAULT 'admin@atlas.ph'"),
        ("fullname", "VARCHAR(200) DEFAULT 'ATLAS Administrator'"),
        ("created",  "DATETIME DEFAULT CURRENT_TIMESTAMP"),
    ]:
        try:
            cur.execute(f"ALTER TABLE admins ADD COLUMN {_col} {_defn}")
            conn.commit()
        except Exception:
            pass  # column already exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_sessions (
            token    VARCHAR(64) PRIMARY KEY,
            admin_id INT         NOT NULL,
            created  DATETIME    DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS spots (
            id     INT AUTO_INCREMENT PRIMARY KEY,
            name   VARCHAR(200) NOT NULL,
            city   VARCHAR(100) NOT NULL,
            cat    VARCHAR(100) NOT NULL,
            rating FLOAT        DEFAULT 4.5,
            entry  VARCHAR(100) DEFAULT 'Free',
            hours  VARCHAR(100) DEFAULT '8AM-6PM',
            descr  TEXT,
            visits VARCHAR(50)  DEFAULT 'N/A'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id     INT AUTO_INCREMENT PRIMARY KEY,
            name   VARCHAR(200) NOT NULL,
            city   VARCHAR(100) NOT NULL,
            type   VARCHAR(100) NOT NULL,
            price  VARCHAR(100) DEFAULT 'Check restaurant',
            rating FLOAT        DEFAULT 4.0
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pending_users (
            id       INT AUTO_INCREMENT PRIMARY KEY,
            fname    VARCHAR(100) NOT NULL,
            lname    VARCHAR(100) NOT NULL,
            email    VARCHAR(255) NOT NULL,
            password VARCHAR(64)  NOT NULL,
            code     VARCHAR(10)  NOT NULL,
            created  DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    # Note: default admin account is seeded by admin_db.init_admin()
    conn.commit()
    cur.close(); conn.close()


# ── USER AUTH ──
def register_user(fname, lname, email, password):
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("INSERT INTO users (fname,lname,email,password) VALUES (%s,%s,%s,%s)",
                    (fname.strip(), lname.strip(), email.strip().lower(), hash_pw(password)))
        conn.commit(); cur.close(); conn.close()
        return True, "Account created!"
    except IntegrityError:
        return False, "Email already registered."
    except Exception as e:
        return False, str(e)

def login_user(email, password):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM users WHERE email=%s",
                (email.strip().lower(),))
    user = cur.fetchone()
    cur.close(); conn.close()
    if user and not check_pw(password, user["password"]):
        user = None
    if not user:
        return False, None, None
    if user.get("status", "active") == "suspended":
        return "suspended", None, None
    # Re-hash with bcrypt if user still has a legacy SHA-256 hash
    if not user["password"].startswith("$2"):
        conn2 = get_conn(); cur2 = _cursor(conn2)
        cur2.execute("UPDATE users SET password=%s WHERE id=%s", (hash_pw(password), user["id"]))
        conn2.commit(); cur2.close(); conn2.close()
    token = secrets.token_hex(32)
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO sessions (token,user_id) VALUES (%s,%s)", (token, user["id"]))
    conn.commit(); cur.close(); conn.close()
    return True, token, user

def get_user_by_email(email):
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("SELECT * FROM users WHERE email=%s", (email.strip().lower(),))
        row = cur.fetchone(); cur.close(); conn.close()
        return row
    except: return None

def get_user_by_token(token):
    if not token: return None
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("""SELECT u.* FROM users u
            JOIN sessions s ON s.user_id=u.id
            WHERE s.token=%s
            AND s.created > NOW() - INTERVAL 24 HOUR""", (token,))
        row = cur.fetchone()
        cur.close(); conn.close()
        return row
    except: return None

def purge_expired_sessions():
    """Delete sessions older than 24 hours. Call periodically on startup."""
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("DELETE FROM sessions WHERE created < NOW() - INTERVAL 24 HOUR")
        cur.execute("DELETE FROM admin_sessions WHERE created < NOW() - INTERVAL 24 HOUR")
        conn.commit(); cur.close(); conn.close()
    except: pass

def logout(token):
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("DELETE FROM sessions WHERE token=%s", (token,))
        conn.commit(); cur.close(); conn.close()
    except: pass


# ── ADMIN AUTH ──
def admin_login(username, password):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM admins WHERE username=%s",
                (username.strip(),))
    admin = cur.fetchone()
    cur.close(); conn.close()
    if not admin or not check_pw(password, admin["password"]):
        return False, None
    token = secrets.token_hex(32)
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO admin_sessions (token,admin_id) VALUES (%s,%s)", (token, admin["id"]))
    conn.commit(); cur.close(); conn.close()
    return True, token
    return False, None

def get_admin_by_token(token):
    if not token: return None
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("""SELECT a.* FROM admins a
            JOIN admin_sessions s ON s.admin_id=a.id
            WHERE s.token=%s
            AND s.created > NOW() - INTERVAL 24 HOUR""", (token,))
        row = cur.fetchone()
        cur.close(); conn.close()
        return row
    except: return None

def admin_logout(token):
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("DELETE FROM admin_sessions WHERE token=%s", (token,))
        conn.commit(); cur.close(); conn.close()
    except: pass


# ── USER MANAGEMENT ──
def get_all_users():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM users ORDER BY created DESC")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def suspend_user(uid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE users SET status='suspended' WHERE id=%s", (uid,))
    conn.commit(); cur.close(); conn.close()

def unsuspend_user(uid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE users SET status='active' WHERE id=%s", (uid,))
    conn.commit(); cur.close(); conn.close()

def delete_user(uid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("DELETE FROM sessions WHERE user_id=%s", (uid,))
    cur.execute("DELETE FROM users WHERE id=%s", (uid,))
    conn.commit(); cur.close(); conn.close()


# ── STATS ──
def get_stats():
    conn = get_conn(); cur = _cursor(conn)
    def count(sql):
        try: cur.execute(sql); return cur.fetchone()[list(cur.fetchone() or {}).pop()] if False else (cur.execute(sql) or cur.fetchone() or {}).get("cnt", 0)
        except: return 0
    cur.execute("SELECT COUNT(*) AS cnt FROM users");            total_users  = (cur.fetchone() or {}).get("cnt", 0)
    cur.execute("SELECT COUNT(*) AS cnt FROM users WHERE status='active'"); active_users = (cur.fetchone() or {}).get("cnt", 0)
    cur.execute("SELECT COUNT(*) AS cnt FROM users WHERE status='suspended'"); suspended = (cur.fetchone() or {}).get("cnt", 0)
    cur.execute("SELECT COUNT(*) AS cnt FROM spots");            total_spots  = (cur.fetchone() or {}).get("cnt", 0)
    cur.execute("SELECT COUNT(*) AS cnt FROM restaurants");      total_rests  = (cur.fetchone() or {}).get("cnt", 0)
    cur.close(); conn.close()
    return {"total_users": total_users, "active_users": active_users,
            "suspended": suspended, "total_spots": total_spots, "total_rests": total_rests}


# ── SPOTS CRUD ──
def get_all_spots():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM spots ORDER BY id DESC")
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def add_spot(data):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO spots (name,city,cat,rating,entry,hours,descr) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (data["name"], data["city"], data["cat"], float(data.get("rating", 4.5)),
                 data.get("entry", "Free"), data.get("hours", "8AM-6PM"), data.get("desc", "")))
    conn.commit(); cur.close(); conn.close()

def delete_spot(sid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("DELETE FROM spots WHERE id=%s", (sid,))
    conn.commit(); cur.close(); conn.close()


# ── RESTAURANTS CRUD ──
def get_all_restaurants():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM restaurants ORDER BY id DESC")
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def add_restaurant(data):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO restaurants (name,city,type,price,rating) VALUES (%s,%s,%s,%s,%s)",
                (data["name"], data["city"], data["type"],
                 data.get("price", "Check restaurant"), float(data.get("rating", 4.0))))
    conn.commit(); cur.close(); conn.close()

def delete_restaurant(rid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("DELETE FROM restaurants WHERE id=%s", (rid,))
    conn.commit(); cur.close(); conn.close()


# ── EMAIL VERIFICATION ──
def email_already_registered(email):
    email = email.strip().lower()
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT COUNT(*) AS cnt FROM users WHERE email=%s", (email,))
    in_users = (cur.fetchone() or {}).get("cnt", 0)
    try:
        cur.execute("SELECT COUNT(*) AS cnt FROM pending_users WHERE email=%s", (email,))
        in_pending = (cur.fetchone() or {}).get("cnt", 0)
    except:
        in_pending = 0
    cur.close(); conn.close()
    return (in_users + in_pending) > 0

def store_pending_user(fname, lname, email, password):
    import random
    code  = str(random.randint(100000, 999999))
    email = email.strip().lower()
    conn  = get_conn(); cur = _cursor(conn)
    try:
        cur.execute("DELETE FROM pending_users WHERE email=%s", (email,))
    except: pass
    cur.execute(
        "INSERT INTO pending_users (fname,lname,email,password,code) VALUES (%s,%s,%s,%s,%s)",
        (fname.strip(), lname.strip(), email, hash_pw(password), code)
    )
    conn.commit(); cur.close(); conn.close()
    return code

def activate_user(email, code):
    email = email.strip().lower()
    conn  = get_conn(); cur = _cursor(conn)
    try:
        cur.execute("SELECT * FROM pending_users WHERE email=%s AND code=%s", (email, code))
        row = cur.fetchone()
        if not row:
            cur.close(); conn.close()
            return False, "Invalid or expired code. Please try again."
        try:
            cur.execute(
                "INSERT INTO users (fname,lname,email,password) VALUES (%s,%s,%s,%s)",
                (row["fname"], row["lname"], row["email"], row["password"])
            )
        except IntegrityError:
            pass
        cur.execute("DELETE FROM pending_users WHERE email=%s", (email,))
        conn.commit(); cur.close(); conn.close()
        return True, "Email verified! Your account is now active."
    except Exception as e:
        cur.close(); conn.close()
        return False, f"Verification error: {e}"

def clear_pending_by_email(email):
    email = email.strip().lower()
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("DELETE FROM pending_users WHERE email=%s", (email,))
        conn.commit(); cur.close(); conn.close()
    except: pass

# ── 2FA / TOTP ──────────────────────────────────────────────────────────────
def set_totp_secret(user_id, secret):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE users SET totp_secret=%s WHERE id=%s", (secret, user_id))
    conn.commit(); cur.close(); conn.close()

def enable_totp(user_id, enabled: bool):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE users SET totp_enabled=%s WHERE id=%s", (1 if enabled else 0, user_id))
    conn.commit(); cur.close(); conn.close()

# ── View history ─────────────────────────────────────────────────────────────
def log_view(user_id, item_type, item_name, item_city="", item_extra=""):
    """Log that a tourist viewed an item. Keeps last 50 entries per user."""
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute(
            "INSERT INTO view_history (user_id,item_type,item_name,item_city,item_extra) VALUES (%s,%s,%s,%s,%s)",
            (user_id, item_type, item_name[:200], item_city[:100], item_extra[:300])
        )
        # Keep only the 50 most recent per user
        cur.execute("""DELETE FROM view_history WHERE user_id=%s AND id NOT IN (
            SELECT id FROM (SELECT id FROM view_history WHERE user_id=%s
                            ORDER BY viewed_at DESC LIMIT 50) AS t)""",
            (user_id, user_id))
        conn.commit(); cur.close(); conn.close()
    except: pass

def get_view_history(user_id, limit=20):
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("""SELECT * FROM view_history WHERE user_id=%s
                       ORDER BY viewed_at DESC LIMIT %s""", (user_id, limit))
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
    except: return []

# ── Flight bookings ──────────────────────────────────────────────────────────
def book_flight(user_id, airline, origin, destination, dep_time, arr_time, flight_number=""):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("""INSERT INTO flight_bookings
        (user_id,airline,origin,destination,dep_time,arr_time,flight_number)
        VALUES (%s,%s,%s,%s,%s,%s,%s)""",
        (user_id, airline, origin, destination, dep_time, arr_time, flight_number))
    conn.commit()
    bid = cur.lastrowid
    cur.close(); conn.close()
    return bid

def get_flight_bookings(user_id):
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("SELECT * FROM flight_bookings WHERE user_id=%s ORDER BY booked_at DESC", (user_id,))
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
    except: return []

def update_flight_booking_status(booking_id, status):
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("UPDATE flight_bookings SET status=%s WHERE id=%s", (status, booking_id))
        conn.commit(); cur.close(); conn.close()
    except: pass

def google_login_or_register(email, fname, lname, photo_url=""):
    """Find or create a user from Google OAuth, then return a session token."""
    import secrets as _sec
    email = email.strip().lower()
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    if not user:
        random_pw = hash_pw(_sec.token_hex(32))
        cur.execute(
            "INSERT INTO users (fname,lname,email,password,photo_url,status) VALUES (%s,%s,%s,%s,%s,'active')",
            (fname or "Google", lname or "User", email, random_pw, photo_url or "")
        )
        conn.commit()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
    if not user or user.get("status") == "suspended":
        cur.close(); conn.close()
        return None, None
    token = _sec.token_hex(32)
    cur.execute("INSERT INTO sessions (token,user_id) VALUES (%s,%s)", (token, user["id"]))
    conn.commit(); cur.close(); conn.close()
    return token, user

# ── INIT ── (called at module load)
init_db()
