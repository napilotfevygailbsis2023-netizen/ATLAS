import sqlite3
import hashlib
import secrets
import os

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

def init_admin():
    """Initialize admin tables"""
    conn = get_conn()
    cur = conn.cursor()
    
    # Admin table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Admin sessions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_sessions (
            token VARCHAR(64) PRIMARY KEY,
            admin_id INTEGER NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tourists table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tourists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname VARCHAR(100) NOT NULL,
            lname VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            phone VARCHAR(50) DEFAULT '',
            status VARCHAR(20) DEFAULT 'active',
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def admin_login(username, password):
    """Admin login"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM admins WHERE username = ? AND password = ?", 
                   (username, hash_pw(password)))
        admin = cur.fetchone()
        
        if admin:
            token = secrets.token_urlsafe(32)
            cur.execute("INSERT INTO admin_sessions (token, admin_id) VALUES (?, ?)", 
                       (token, admin['id']))
            conn.commit()
            conn.close()
            return True, token, dict(admin)
        
        conn.close()
        return False, None, None
        
    except Exception as e:
        print(f"Admin login error: {e}")
        return False, None, None

def get_admin_by_token(token):
    """Get admin from session token"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT a.* FROM admins a
            JOIN admin_sessions s ON a.id = s.admin_id
            WHERE s.token = ?
        """, (token,))
        
        admin = cur.fetchone()
        conn.close()
        
        return dict(admin) if admin else None
        
    except Exception as e:
        print(f"Admin token validation error: {e}")
        return None

def admin_logout(token):
    """Logout admin"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM admin_sessions WHERE token = ?", (token,))
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Admin logout error: {e}")
        return False

def get_all_tourists():
    """Get all tourists"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM tourists ORDER BY created DESC")
        tourists = cur.fetchall()
        conn.close()
        
        return [dict(t) for t in tourists]
        
    except Exception as e:
        print(f"Error getting tourists: {e}")
        return []

def set_tourist_status(tourist_id, status):
    """Set tourist status"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("UPDATE tourists SET status = ? WHERE id = ?", (status, tourist_id))
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error setting tourist status: {e}")
        return False

def delete_tourist(tourist_id):
    """Delete tourist"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM tourists WHERE id = ?", (tourist_id,))
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error deleting tourist: {e}")
        return False

# Initialize tables on import
init_admin()
