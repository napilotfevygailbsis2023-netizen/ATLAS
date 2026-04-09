import sqlite3
import hashlib
import secrets
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'atlas.db')

def get_conn():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _cursor(conn):
    """Get cursor from connection"""
    return conn.cursor()

def hash_pw(p):
    """Hash password"""
    return hashlib.sha256(p.encode()).hexdigest()

def init_guide_tables():
    """Initialize guide tables"""
    conn = get_conn()
    cur = conn.cursor()
    
    # Tour guides table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tour_guides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname VARCHAR(100) NOT NULL,
            lname VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            phone VARCHAR(50) DEFAULT '',
            city VARCHAR(100) DEFAULT 'Manila',
            languages VARCHAR(200) DEFAULT 'EN, FIL',
            speciality VARCHAR(200) DEFAULT 'General Tours',
            bio TEXT,
            rate VARCHAR(100) DEFAULT 'P1,500/day',
            availability VARCHAR(200) DEFAULT 'Mon-Sun',
            photo_url VARCHAR(500) DEFAULT '',
            status VARCHAR(20) DEFAULT 'active',
            permit_number VARCHAR(100),
            permit_expiry DATE,
            license_number VARCHAR(100),
            license_expiry DATE,
            verification_status VARCHAR(20) DEFAULT 'pending',
            permit_document VARCHAR(500),
            license_document VARCHAR(500),
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Guide sessions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS guide_sessions (
            token VARCHAR(64) PRIMARY KEY,
            guide_id INTEGER NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tour packages table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tour_packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guide_id INTEGER NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            price VARCHAR(100) NOT NULL,
            duration VARCHAR(100) DEFAULT 'Full Day',
            inclusions TEXT,
            city VARCHAR(100) DEFAULT 'Manila',
            status VARCHAR(20) DEFAULT 'active',
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Bookings table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guide_id INTEGER NOT NULL,
            tourist_name VARCHAR(200) NOT NULL,
            tourist_email VARCHAR(255) DEFAULT '',
            tourist_phone VARCHAR(50) DEFAULT '',
            package_id INTEGER DEFAULT 0,
            package_title VARCHAR(200) DEFAULT '',
            tour_date VARCHAR(20) NOT NULL,
            pax INTEGER DEFAULT 1,
            notes TEXT,
            status VARCHAR(20) DEFAULT 'pending',
            guide_notes TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Guide ratings table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS guide_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guide_id INTEGER NOT NULL,
            tourist_name VARCHAR(200) NOT NULL,
            rating INTEGER NOT NULL,
            feedback TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def guide_login(email, password):
    """Guide login"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM tour_guides WHERE email = ? AND password = ?", 
                   (email, hash_pw(password)))
        guide = cur.fetchone()
        
        if guide:
            token = secrets.token_urlsafe(32)
            cur.execute("INSERT INTO guide_sessions (token, guide_id) VALUES (?, ?)", 
                       (token, guide['id']))
            conn.commit()
            conn.close()
            return True, token, dict(guide)
        
        conn.close()
        return False, None, None
        
    except Exception as e:
        print(f"Guide login error: {e}")
        return False, None, None

def get_guide_from_token(token):
    """Get guide from session token"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT g.* FROM tour_guides g
            JOIN guide_sessions s ON g.id = s.guide_id
            WHERE s.token = ?
        """, (token,))
        
        guide = cur.fetchone()
        conn.close()
        
        return dict(guide) if guide else None
        
    except Exception as e:
        print(f"Guide token validation error: {e}")
        return None

def get_public_guides(city=None):
    """Get public guides"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        if city:
            cur.execute("SELECT * FROM tour_guides WHERE status='active' AND city=? ORDER BY id DESC", (city,))
        else:
            cur.execute("SELECT * FROM tour_guides WHERE status='active' ORDER BY id DESC")
        
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]
        
    except Exception as e:
        print(f"Error getting guides: {e}")
        return []

def get_packages(guide_id):
    """Get guide packages"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM tour_packages WHERE guide_id=? AND status='active'", (guide_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]
        
    except Exception as e:
        print(f"Error getting packages: {e}")
        return []

def get_avg_rating(guide_id):
    """Get average rating for guide"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT AVG(rating) as avg, COUNT(*) as count FROM guide_ratings WHERE guide_id=?", (guide_id,))
        result = cur.fetchone()
        conn.close()
        
        if result and result['count'] > 0:
            return float(result['avg']), int(result['count'])
        return 4.5, 0
        
    except Exception as e:
        print(f"Error getting rating: {e}")
        return 4.5, 0

def get_completed_tours_count(guide_id):
    """Get completed tours count for guide"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) as count FROM bookings WHERE guide_id=? AND status='completed'", (guide_id,))
        result = cur.fetchone()
        conn.close()
        
        return result['count'] if result else 0
        
    except Exception as e:
        print(f"Error getting completed tours: {e}")
        return 0

def create_booking(guide_id, tourist_name, tourist_email, tourist_phone, package_title, tour_date, notes):
    """Create a new booking"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO bookings 
            (guide_id, tourist_name, tourist_email, tourist_phone, package_title, tour_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (guide_id, tourist_name, tourist_email, tourist_phone, package_title, tour_date, notes))
        
        booking_id = cur.lastrowid
        conn.commit()
        conn.close()
        
        return booking_id
        
    except Exception as e:
        print(f"Error creating booking: {e}")
        return None

def get_bookings_by_tourist_email(tourist_email):
    """Get bookings by tourist email"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT b.*, g.fname as gfname, g.lname as glname 
            FROM bookings b
            LEFT JOIN tour_guides g ON b.guide_id = g.id
            WHERE b.tourist_email = ?
            ORDER BY b.created DESC
        """, (tourist_email,))
        
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]
        
    except Exception as e:
        print(f"Error getting tourist bookings: {e}")
        return []

# Initialize tables on import
init_guide_tables()
