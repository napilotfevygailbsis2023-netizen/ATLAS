import hashlib, secrets
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
    return hashlib.sha256(p.encode()).hexdigest()

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
            status       VARCHAR(20)  DEFAULT 'active',
            created      DATETIME     DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
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
            pass
        cur.execute("DELETE FROM pending_guides WHERE email=%s", (email,))
        conn.commit(); cur.close(); conn.close()
        return True, "Email verified! Your guide account is now active."
    except Exception as e:
        cur.close(); conn.close()
        return False, f"Verification error: {e}"

def register_guide(fname, lname, email, password, phone, city):
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("INSERT INTO tour_guides (fname,lname,email,password,phone,city) VALUES (%s,%s,%s,%s,%s,%s)",
                    (fname.strip(), lname.strip(), email.strip().lower(), hash_pw(password), phone.strip(), city))
        conn.commit(); cur.close(); conn.close()
        return True, "Account created!"
    except IntegrityError:
        return False, "Email already registered."
    except Exception as e:
        return False, str(e)

def login_guide(email, password):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM tour_guides WHERE email=%s AND password=%s",
                (email.strip().lower(), hash_pw(password)))
    guide = cur.fetchone(); cur.close(); conn.close()
    if not guide: return False, None, None
    token = secrets.token_hex(32)
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO guide_sessions (token,guide_id) VALUES (%s,%s)", (token, guide["id"]))
    conn.commit(); cur.close(); conn.close()
    return True, token, guide

def get_guide_by_token(token):
    if not token: return None
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("""SELECT g.* FROM tour_guides g
            JOIN guide_sessions s ON s.guide_id=g.id WHERE s.token=%s""", (token,))
        row = cur.fetchone(); cur.close(); conn.close()
        return row
    except: return None

def logout_guide(token):
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("DELETE FROM guide_sessions WHERE token=%s", (token,))
        conn.commit(); cur.close(); conn.close()
    except: pass

def get_guide_by_id(gid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM tour_guides WHERE id=%s", (gid,))
    row = cur.fetchone(); cur.close(); conn.close()
    return row

def update_guide_profile(gid, data):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("""UPDATE tour_guides SET fname=%s,lname=%s,phone=%s,city=%s,languages=%s,
        speciality=%s,bio=%s,rate=%s,availability=%s WHERE id=%s""",
        (data["fname"], data["lname"], data["phone"], data["city"], data["languages"],
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

def add_booking(data):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("""INSERT INTO bookings (guide_id,tourist_name,tourist_email,tourist_phone,
        package_id,package_title,tour_date,pax,notes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (data["guide_id"], data["tourist_name"], data.get("tourist_email",""),
         data.get("tourist_phone",""), data.get("package_id",0), data.get("package_title",""),
         data["tour_date"], int(data.get("pax",1)), data.get("notes","")))
    conn.commit(); cur.close(); conn.close()

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

init_guide_tables()
