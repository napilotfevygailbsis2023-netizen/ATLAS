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
    return conn.cursor(dictionary=True)

def hash_pw(p):
    """Hash a password with bcrypt (salted). Returns a str for DB storage."""
    return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

def check_pw(plain, hashed):
    """Verify a plain password against a bcrypt or legacy SHA-256 hash."""
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return hashlib.sha256(plain.encode()).hexdigest() == hashed

def init_guide_tables():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tour_guides (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            fname        VARCHAR(100) NOT NULL,
            lname        VARCHAR(100) NOT NULL,
            email        VARCHAR(255) UNIQUE NOT NULL,
            password     VARCHAR(64)  NOT NULL,
            phone        VARCHAR(50)  DEFAULT '',
            city         VARCHAR(100) DEFAULT 'Manila',
            languages    VARCHAR(200) DEFAULT 'EN, FIL',
            speciality   VARCHAR(200) DEFAULT 'General Tours',
            bio          TEXT,
            rate         VARCHAR(100) DEFAULT 'P1,500/day',
            availability VARCHAR(200) DEFAULT 'Mon-Sun',
            avail_note   VARCHAR(500) DEFAULT '',
            photo_url    VARCHAR(500) DEFAULT '',
            doc_url      VARCHAR(500) DEFAULT '',
            doc_status   VARCHAR(20)  DEFAULT 'none',
            doc_ai_notes TEXT,
            totp_secret  VARCHAR(64)  DEFAULT '',
            totp_enabled TINYINT(1)   DEFAULT 0,
            status       VARCHAR(20)  DEFAULT 'pending',
            created      DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    try:
        cur.execute("ALTER TABLE tour_guides ADD COLUMN photo_url VARCHAR(500) DEFAULT ''")
        conn.commit()
    except Exception:
        pass  # Column already exists
    try:
        cur.execute("ALTER TABLE tour_guides ADD COLUMN avail_note VARCHAR(500) DEFAULT ''")
        conn.commit()
    except Exception:
        pass  # Column already exists
    for _col, _defn in [
        ("doc_url",      "VARCHAR(500) DEFAULT ''"),
        ("doc_status",   "VARCHAR(20) DEFAULT 'none'"),
        ("doc_ai_notes", "TEXT"),
        ("totp_secret",  "VARCHAR(64) DEFAULT ''"),
        ("totp_enabled", "TINYINT(1) DEFAULT 0"),
    ]:
        try:
            cur.execute(f"ALTER TABLE tour_guides ADD COLUMN {_col} {_defn}")
            conn.commit()
        except Exception:
            pass
    cur.execute("""
        CREATE TABLE IF NOT EXISTS guide_sessions (
            token    VARCHAR(64) PRIMARY KEY,
            guide_id INT         NOT NULL,
            created  DATETIME    DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tour_packages (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            guide_id    INT          NOT NULL,
            title       VARCHAR(200) NOT NULL,
            description TEXT,
            price       VARCHAR(100) NOT NULL,
            duration    VARCHAR(100) DEFAULT 'Full Day',
            inclusions  TEXT,
            city        VARCHAR(100) DEFAULT 'Manila',
            status      VARCHAR(20)  DEFAULT 'active',
            created     DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            guide_id      INT          NOT NULL,
            tourist_name  VARCHAR(200) NOT NULL,
            tourist_email VARCHAR(255) DEFAULT '',
            tourist_phone VARCHAR(50)  DEFAULT '',
            package_id    INT          DEFAULT 0,
            package_title VARCHAR(200) DEFAULT '',
            tour_date     VARCHAR(20)  NOT NULL,
            pax           INT          DEFAULT 1,
            notes         TEXT,
            status        VARCHAR(20)  DEFAULT 'pending',
            guide_notes   TEXT,
            created       DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    try:
        cur.execute("ALTER TABLE bookings ADD COLUMN guide_notes TEXT")
        conn.commit()
    except Exception:
        pass  # Already exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS guide_ratings (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            guide_id     INT          NOT NULL,
            tourist_name VARCHAR(200) NOT NULL,
            rating       INT          NOT NULL,
            feedback     TEXT,
            created      DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pending_guides (
            id       INT AUTO_INCREMENT PRIMARY KEY,
            fname    VARCHAR(100) NOT NULL,
            lname    VARCHAR(100) NOT NULL,
            email    VARCHAR(255) NOT NULL,
            password VARCHAR(64)  NOT NULL,
            phone    VARCHAR(50)  DEFAULT '',
            city     VARCHAR(100) DEFAULT 'Manila',
            code     VARCHAR(10)  NOT NULL,
            created  DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    # Table for pending email-OTP 2FA codes (login step)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS guide_otp_pending (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            guide_id   INT         NOT NULL,
            code       VARCHAR(10) NOT NULL,
            expires_at DATETIME    NOT NULL,
            created    DATETIME    DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY uq_guide (guide_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    conn.commit(); cur.close(); conn.close()


def guide_email_registered(email):
    email = email.strip().lower()
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT COUNT(*) AS cnt FROM tour_guides WHERE email=%s", (email,))
    in_guides = (cur.fetchone() or {}).get("cnt", 0)
    try:
        cur.execute("SELECT COUNT(*) AS cnt FROM pending_guides WHERE email=%s", (email,))
        in_pending = (cur.fetchone() or {}).get("cnt", 0)
    except:
        in_pending = 0
    cur.close(); conn.close()
    return (in_guides + in_pending) > 0

def store_pending_guide(fname, lname, email, password, phone, city):
    import random
    code = str(random.randint(100000, 999999))
    email = email.strip().lower()
    conn = get_conn(); cur = _cursor(conn)
    try: cur.execute("DELETE FROM pending_guides WHERE email=%s", (email,))
    except: pass
    cur.execute(
        "INSERT INTO pending_guides (fname,lname,email,password,phone,city,code) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (fname.strip(), lname.strip(), email, hash_pw(password), phone.strip(), city, code)
    )
    conn.commit(); cur.close(); conn.close()
    return code

def activate_guide(email, code):
    email = email.strip().lower()
    conn = get_conn(); cur = _cursor(conn)
    try:
        cur.execute("SELECT * FROM pending_guides WHERE email=%s AND code=%s", (email, code))
        row = cur.fetchone()
        if not row:
            cur.close(); conn.close()
            return False, "Invalid or expired code. Please try again."
        try:
            cur.execute(
                "INSERT INTO tour_guides (fname,lname,email,password,phone,city) VALUES (%s,%s,%s,%s,%s,%s)",
                (row["fname"], row["lname"], row["email"], row["password"], row["phone"], row["city"])
            )
        except IntegrityError:
            cur.close(); conn.close()
            return False, "Email already registered."
        cur.execute("DELETE FROM pending_guides WHERE email=%s", (email,))
        conn.commit(); cur.close(); conn.close()
        return True, "Account activated successfully."
    except Exception as e:
        try: conn.rollback()
        except: pass
        try: cur.close(); conn.close()
        except: pass
        return False, str(e)

def register_guide(fname, lname, email, password, phone, city):
    """Directly register a guide into tour_guides (used for Google OAuth auto-creation).
    Inserts with status='pending' so the guide can log in immediately but is
    flagged for admin review. Returns (True, '') on success or (False, reason) on failure.
    """
    email = email.strip().lower()
    conn = get_conn(); cur = _cursor(conn)
    try:
        cur.execute(
            "INSERT INTO tour_guides (fname,lname,email,password,phone,city) VALUES (%s,%s,%s,%s,%s,%s)",
            (fname.strip(), lname.strip(), email, hash_pw(password), phone.strip(), city)
        )
        conn.commit(); cur.close(); conn.close()
        return True, ""
    except IntegrityError:
        try: cur.close(); conn.close()
        except: pass
        return False, "Email already registered."
    except Exception as ex:
        try: conn.rollback(); cur.close(); conn.close()
        except: pass
        return False, str(ex)

def get_guide_by_email(email):
    email = email.strip().lower()
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM tour_guides WHERE email=%s", (email,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row

def get_guide_by_id(guide_id):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM tour_guides WHERE id=%s", (guide_id,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row

def login_guide(email, password):
    guide = get_guide_by_email(email)
    if not guide:
        return False, None, None
    if not check_pw(password, guide["password"]):
        return False, None, None
    tok = secrets.token_hex(32)
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO guide_sessions (token,guide_id) VALUES (%s,%s)", (tok, guide["id"]))
    conn.commit(); cur.close(); conn.close()
    return True, tok, guide

def create_guide_session(guide_id):
    """Create a new session token for a guide and return the token."""
    tok = secrets.token_hex(32)
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO guide_sessions (token,guide_id) VALUES (%s,%s)", (tok, guide_id))
    conn.commit(); cur.close(); conn.close()
    return tok

def get_guide_by_token(token):
    if not token: return None
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("""
        SELECT g.* FROM tour_guides g
        JOIN guide_sessions s ON s.guide_id=g.id
        WHERE s.token=%s
    """, (token,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row

def logout_guide(token):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("DELETE FROM guide_sessions WHERE token=%s", (token,))
    conn.commit(); cur.close(); conn.close()

def purge_expired_guide_sessions():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("DELETE FROM guide_sessions WHERE created < NOW() - INTERVAL 30 DAY")
    conn.commit(); cur.close(); conn.close()

def update_guide_profile(gid, data):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("""
        UPDATE tour_guides SET phone=%s,city=%s,languages=%s,speciality=%s,bio=%s,rate=%s,availability=%s WHERE id=%s
    """, (data["phone"], data["city"], data["languages"],
         data["speciality"], data["bio"], data["rate"], data["availability"], gid))
    conn.commit(); cur.close(); conn.close()

def change_guide_password(gid, new_pw):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE tour_guides SET password=%s WHERE id=%s", (hash_pw(new_pw), gid))
    conn.commit(); cur.close(); conn.close()

def get_packages(guide_id):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM tour_packages WHERE guide_id=%s ORDER BY id DESC", (guide_id,))
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def add_package(guide_id, data):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO tour_packages (guide_id,title,description,price,duration,inclusions,city) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (guide_id, data["title"], data.get("description",""), data["price"],
                 data.get("duration","Full Day"), data.get("inclusions",""), data.get("city","Manila")))
    conn.commit(); cur.close(); conn.close()

def delete_package(pkg_id, guide_id):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("DELETE FROM tour_packages WHERE id=%s AND guide_id=%s", (pkg_id, guide_id))
    conn.commit(); cur.close(); conn.close()

def get_bookings(guide_id, status=None):
    conn = get_conn(); cur = _cursor(conn)
    if status:
        cur.execute("SELECT * FROM bookings WHERE guide_id=%s AND status=%s ORDER BY tour_date ASC", (guide_id, status))
    else:
        cur.execute("SELECT * FROM bookings WHERE guide_id=%s ORDER BY tour_date ASC", (guide_id,))
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def update_booking_status(booking_id, guide_id, status, notes=""):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE bookings SET status=%s, guide_notes=%s WHERE id=%s AND guide_id=%s",
                (status, notes, booking_id, guide_id))
    conn.commit(); cur.close(); conn.close()

def update_guide_photo(guide_id, photo_url):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE tour_guides SET photo_url=%s WHERE id=%s", (photo_url, guide_id))
    conn.commit(); cur.close(); conn.close()

def reschedule_booking(booking_id, guide_id, new_date):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE bookings SET status='rescheduled', tour_date=%s WHERE id=%s AND guide_id=%s",
                (new_date, booking_id, guide_id))
    conn.commit(); cur.close(); conn.close()

def add_booking(data):
    guide_id      = int(data.get("guide_id", 0))
    tourist_name  = str(data.get("tourist_name", "")).strip()
    tourist_email = str(data.get("tourist_email", "")).strip()
    tourist_phone = str(data.get("tourist_phone", "")).strip()
    package_id    = int(data.get("package_id", 0))
    package_title = str(data.get("package_title", "")).strip()
    tour_date     = str(data.get("tour_date", "")).strip()
    pax           = int(data.get("pax", 1))
    notes         = str(data.get("notes", "")).strip()

    if not guide_id:
        raise ValueError("add_booking: guide_id is 0 or missing — booking aborted.")
    if not tourist_name:
        raise ValueError("add_booking: tourist_name is empty — booking aborted.")
    if not tour_date:
        raise ValueError("add_booking: tour_date is empty — booking aborted.")

    conn = get_conn(); cur = _cursor(conn)
    try:
        cur.execute(
            """INSERT INTO bookings
               (guide_id, tourist_name, tourist_email, tourist_phone,
                package_id, package_title, tour_date, pax, notes)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (guide_id, tourist_name, tourist_email, tourist_phone,
             package_id, package_title, tour_date, pax, notes)
        )
        conn.commit()
    except Exception:
        import traceback; traceback.print_exc()
        raise
    finally:
        cur.close(); conn.close()

def get_bookings_by_tourist_email(email):
    """Return all bookings for a tourist identified by email, newest first."""
    if not email:
        return []
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("""
        SELECT b.*, g.fname, g.lname, g.phone AS guide_phone,
               g.city AS guide_city, g.photo_url AS guide_photo
        FROM bookings b
        JOIN tour_guides g ON g.id = b.guide_id
        WHERE b.tourist_email = %s
        ORDER BY b.created DESC
    """, (email.strip().lower(),))
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def get_completed_tours_count(guide_id):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT COUNT(*) AS cnt FROM bookings WHERE guide_id=%s AND status='completed'", (guide_id,))
    row = cur.fetchone(); cur.close(); conn.close()
    return (row or {}).get("cnt", 0)

def get_ratings(guide_id):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM guide_ratings WHERE guide_id=%s ORDER BY created DESC", (guide_id,))
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def add_rating(guide_id, tourist_name, rating, feedback):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO guide_ratings (guide_id,tourist_name,rating,feedback) VALUES (%s,%s,%s,%s)",
                (guide_id, tourist_name, int(rating), feedback))
    conn.commit(); cur.close(); conn.close()

def get_avg_rating(guide_id):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT AVG(rating) AS avg_r, COUNT(*) AS cnt FROM guide_ratings WHERE guide_id=%s", (guide_id,))
    row = cur.fetchone(); cur.close(); conn.close()
    return round(float(row["avg_r"] or 0), 1), row["cnt"]

def get_public_guides(city=None):
    conn = get_conn(); cur = _cursor(conn)
    if city and city != "All":
        cur.execute("SELECT * FROM tour_guides WHERE status='active' AND city=%s ORDER BY id DESC", (city,))
    else:
        cur.execute("SELECT * FROM tour_guides WHERE status='active' ORDER BY id DESC")
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

# ── Document validation ──────────────────────────────────────────────────────
def save_guide_doc(guide_id, doc_url):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE tour_guides SET doc_url=%s, doc_status='pending', doc_ai_notes='' WHERE id=%s",
                (doc_url, guide_id))
    conn.commit(); cur.close(); conn.close()

def update_doc_status(guide_id, status, ai_notes=""):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE tour_guides SET doc_status=%s, doc_ai_notes=%s WHERE id=%s",
                (status, ai_notes, guide_id))
    conn.commit(); cur.close(); conn.close()

def get_guides_with_pending_docs():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM tour_guides WHERE doc_status='pending' ORDER BY created DESC")
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

# ── Guide Email OTP 2FA ──────────────────────────────────────────────────────

def enable_guide_2fa(guide_id, enabled: bool):
    """Turn email-OTP 2FA on or off for a guide."""
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE tour_guides SET totp_enabled=%s WHERE id=%s", (1 if enabled else 0, guide_id))
    conn.commit(); cur.close(); conn.close()

def create_guide_otp(guide_id) -> str:
    """Generate a 6-digit OTP, store it (expires in 10 min), and return the code."""
    import random
    code = str(random.randint(100000, 999999))
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("""
        INSERT INTO guide_otp_pending (guide_id, code, expires_at)
        VALUES (%s, %s, NOW() + INTERVAL 10 MINUTE)
        ON DUPLICATE KEY UPDATE code=VALUES(code), expires_at=VALUES(expires_at), created=NOW()
    """, (guide_id, code))
    conn.commit(); cur.close(); conn.close()
    return code

def verify_guide_otp(guide_id, submitted_code) -> bool:
    """Return True and delete the OTP if it matches and hasn't expired."""
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("""
        SELECT id FROM guide_otp_pending
        WHERE guide_id=%s AND code=%s AND expires_at > NOW()
    """, (guide_id, submitted_code.strip()))
    row = cur.fetchone()
    if row:
        cur.execute("DELETE FROM guide_otp_pending WHERE guide_id=%s", (guide_id,))
        conn.commit()
    cur.close(); conn.close()
    return row is not None


def get_all_guides():
    """Returns ALL tour_guides rows regardless of status (for admin Not Registered tab)."""
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM tour_guides ORDER BY created DESC")
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def set_doc_status(guide_id, status):
    """Alias used by admin panel — sets doc_status only."""
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE tour_guides SET doc_status=%s WHERE id=%s", (status, guide_id))
    conn.commit(); cur.close(); conn.close()

def save_doc_ai_notes(guide_id, notes):
    """Save AI review notes for a guide document."""
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE tour_guides SET doc_ai_notes=%s WHERE id=%s", (notes, guide_id))
    conn.commit(); cur.close(); conn.close()

init_guide_tables()
