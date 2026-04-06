import hashlib, secrets, os
try:
    import bcrypt
except ImportError:
    raise ImportError("bcrypt is not installed. Run: pip install bcrypt")
try:
    import mysql.connector
    from mysql.connector import IntegrityError
except ImportError:
    raise ImportError("Run: pip install mysql-connector-python")

from db_config import DB_CONFIG

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

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

def init_admin():
    conn = get_conn(); cur = _cursor(conn)
    tables = [
        """CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL, email VARCHAR(255) DEFAULT 'admin@atlas.ph',
            fullname VARCHAR(200) DEFAULT 'ATLAS Administrator',
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS admin_sessions (
            token VARCHAR(64) PRIMARY KEY, admin_id INT NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS custom_spots (
            id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(200) NOT NULL,
            city VARCHAR(100) NOT NULL, category VARCHAR(100) NOT NULL, type VARCHAR(100) NOT NULL,
            rating FLOAT DEFAULT 4.0, entry VARCHAR(100) DEFAULT 'Free',
            hours VARCHAR(100) DEFAULT '8AM-5PM', descr TEXT, image_url TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS custom_restaurants (
            id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(200) NOT NULL,
            city VARCHAR(100) NOT NULL, cuisine VARCHAR(100) NOT NULL,
            price VARCHAR(100) DEFAULT 'PHP 200-400', rating FLOAT DEFAULT 4.0,
            hours VARCHAR(100) DEFAULT '10AM-10PM', image_url TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS custom_flights (
            id INT AUTO_INCREMENT PRIMARY KEY, airline VARCHAR(200) NOT NULL,
            origin VARCHAR(200) NOT NULL, dest VARCHAR(200) NOT NULL,
            dep_time VARCHAR(20) NOT NULL, arr_time VARCHAR(20) NOT NULL,
            price VARCHAR(100) DEFAULT 'PHP 2,000', status VARCHAR(50) DEFAULT 'Scheduled',
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS custom_guides (
            id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(200) NOT NULL,
            city VARCHAR(100) NOT NULL, language VARCHAR(200) NOT NULL,
            rate VARCHAR(100) DEFAULT 'PHP 1,500/day', rating FLOAT DEFAULT 4.5,
            bio TEXT, image_url TEXT, created DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
        """CREATE TABLE IF NOT EXISTS custom_transport (
            id INT AUTO_INCREMENT PRIMARY KEY, route VARCHAR(200) NOT NULL,
            type VARCHAR(100) NOT NULL, origin VARCHAR(200) NOT NULL, dest VARCHAR(200) NOT NULL,
            dep_time VARCHAR(20) NOT NULL, fare VARCHAR(100) DEFAULT 'PHP 100',
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    ]
    for t in tables:
        cur.execute(t)
    try: cur.execute("ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active'")
    except: pass
    conn.commit()
    try:
        default_pw = os.environ.get("ATLAS_ADMIN_PASSWORD", "admin123")
        cur.execute("INSERT INTO admins (username,password) VALUES (%s,%s)", ("admin", hash_pw(default_pw)))
        conn.commit()
    except: pass
    cur.close(); conn.close()

def admin_login(username, password):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM admins WHERE username=%s", (username.strip(),))
    row = cur.fetchone(); cur.close(); conn.close()
    if not row or not check_pw(password, row["password"]):
        return None
    token = secrets.token_hex(32)
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO admin_sessions (token,admin_id) VALUES (%s,%s)", (token, row["id"]))
    conn.commit(); cur.close(); conn.close()
    return token
    return None

def get_admin_by_token(token):
    if not token: return None
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("SELECT a.* FROM admins a JOIN admin_sessions s ON s.admin_id=a.id WHERE s.token=%s AND s.created > NOW() - INTERVAL 24 HOUR", (token,))
        row = cur.fetchone(); cur.close(); conn.close()
        return row
    except: return None

def admin_logout(token):
    try:
        conn = get_conn(); cur = _cursor(conn)
        cur.execute("DELETE FROM admin_sessions WHERE token=%s", (token,))
        conn.commit(); cur.close(); conn.close()
    except: pass

def update_admin_profile(admin_id, fullname, email, new_password=None):
    conn = get_conn(); cur = _cursor(conn)
    if new_password:
        cur.execute("UPDATE admins SET fullname=%s,email=%s,password=%s WHERE id=%s", (fullname, email, hash_pw(new_password), admin_id))
    else:
        cur.execute("UPDATE admins SET fullname=%s,email=%s WHERE id=%s", (fullname, email, admin_id))
    conn.commit(); cur.close(); conn.close()

def get_stats():
    conn = get_conn(); cur = _cursor(conn)
    def count(sql):
        try: cur.execute(sql); return (cur.fetchone() or {}).get("cnt", 0)
        except: return 0
    s = {
        "total_tourists":  count("SELECT COUNT(*) AS cnt FROM users"),
        "active_tourists": count("SELECT COUNT(*) AS cnt FROM users WHERE status='active' OR status IS NULL"),
        "suspended":       count("SELECT COUNT(*) AS cnt FROM users WHERE status='suspended'"),
        "total_spots":     count("SELECT COUNT(*) AS cnt FROM custom_spots"),
        "total_rests":     count("SELECT COUNT(*) AS cnt FROM custom_restaurants"),
        "total_flights":   count("SELECT COUNT(*) AS cnt FROM custom_flights"),
        "total_guides":    count("SELECT COUNT(*) AS cnt FROM custom_guides"),
        "total_transport": count("SELECT COUNT(*) AS cnt FROM custom_transport"),
    }
    cur.close(); conn.close(); return s

def get_recent_tourists(limit=5):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT id,fname,lname,email,created,status FROM users ORDER BY created DESC LIMIT %s", (limit,))
    rows = cur.fetchall(); cur.close(); conn.close(); return rows

def get_all_tourists():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT id,fname,lname,email,created,status FROM users ORDER BY created DESC")
    rows = cur.fetchall(); cur.close(); conn.close(); return rows

def set_tourist_status(uid, status):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("UPDATE users SET status=%s WHERE id=%s", (status, uid))
    conn.commit(); cur.close(); conn.close()

def delete_tourist(uid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT email FROM users WHERE id=%s", (uid,))
    row = cur.fetchone()
    cur.execute("DELETE FROM sessions WHERE user_id=%s", (uid,))
    cur.execute("DELETE FROM users WHERE id=%s", (uid,))
    if row:
        try: cur.execute("DELETE FROM pending_users WHERE email=%s", (row["email"],))
        except: pass
        try: cur.execute("DELETE FROM bookings WHERE tourist_email=%s", (row["email"],))
        except: pass
    conn.commit(); cur.close(); conn.close()

def get_spots():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM custom_spots ORDER BY created DESC")
    rows = cur.fetchall(); cur.close(); conn.close(); return rows

def add_spot(name, city, category, stype, rating, entry, hours, desc, image_url=''):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO custom_spots (name,city,category,type,rating,entry,hours,descr,image_url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (name, city, category, stype, float(rating), entry, hours, desc, image_url))
    conn.commit(); cur.close(); conn.close()

def delete_spot(sid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("DELETE FROM custom_spots WHERE id=%s", (sid,))
    conn.commit(); cur.close(); conn.close()

def get_restaurants():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM custom_restaurants ORDER BY created DESC")
    rows = cur.fetchall(); cur.close(); conn.close(); return rows

def add_restaurant(name, city, cuisine, price, rating, hours, image_url=''):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO custom_restaurants (name,city,cuisine,price,rating,hours,image_url) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (name, city, cuisine, price, float(rating), hours, image_url))
    conn.commit(); cur.close(); conn.close()

def delete_restaurant(rid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("DELETE FROM custom_restaurants WHERE id=%s", (rid,))
    conn.commit(); cur.close(); conn.close()

def get_flights():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM custom_flights ORDER BY created DESC")
    rows = cur.fetchall(); cur.close(); conn.close(); return rows

def add_flight(airline, origin, dest, dep_time, arr_time, price, status):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO custom_flights (airline,origin,dest,dep_time,arr_time,price,status) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (airline, origin, dest, dep_time, arr_time, price, status))
    conn.commit(); cur.close(); conn.close()

def delete_flight(fid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("DELETE FROM custom_flights WHERE id=%s", (fid,))
    conn.commit(); cur.close(); conn.close()

def get_guides():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM custom_guides ORDER BY created DESC")
    rows = cur.fetchall(); cur.close(); conn.close(); return rows

def add_guide(name, city, language, rate, rating, bio, image_url=''):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO custom_guides (name,city,language,rate,rating,bio,image_url) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (name, city, language, rate, float(rating), bio, image_url))
    conn.commit(); cur.close(); conn.close()

def delete_guide(gid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("DELETE FROM custom_guides WHERE id=%s", (gid,))
    try:
        cur.execute("SELECT email FROM tour_guides WHERE id=%s", (gid,))
        row = cur.fetchone()
        for sql in ["DELETE FROM guide_sessions WHERE guide_id=%s",
                    "DELETE FROM tour_packages WHERE guide_id=%s",
                    "DELETE FROM bookings WHERE guide_id=%s",
                    "DELETE FROM guide_ratings WHERE guide_id=%s",
                    "DELETE FROM tour_guides WHERE id=%s"]:
            cur.execute(sql, (gid,))
        if row:
            try: cur.execute("DELETE FROM pending_guides WHERE email=%s", (row["email"],))
            except: pass
    except: pass
    conn.commit(); cur.close(); conn.close()

def get_transport():
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("SELECT * FROM custom_transport ORDER BY created DESC")
    rows = cur.fetchall(); cur.close(); conn.close(); return rows

def add_transport(route, ttype, origin, dest, dep_time, fare):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("INSERT INTO custom_transport (route,type,origin,dest,dep_time,fare) VALUES (%s,%s,%s,%s,%s,%s)",
                (route, ttype, origin, dest, dep_time, fare))
    conn.commit(); cur.close(); conn.close()

def delete_transport(tid):
    conn = get_conn(); cur = _cursor(conn)
    cur.execute("DELETE FROM custom_transport WHERE id=%s", (tid,))
    conn.commit(); cur.close(); conn.close()

init_admin()
