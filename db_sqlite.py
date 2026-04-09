import sqlite3
import hashlib
import secrets
import os
import json
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

def init_user_tables():
    """Initialize user tables"""
    conn = get_conn()
    cur = conn.cursor()
    
    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname VARCHAR(100) NOT NULL,
            lname VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            phone VARCHAR(50) DEFAULT '',
            totp_secret VARCHAR(32),
            totp_enabled BOOLEAN DEFAULT 0,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # User sessions table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            token VARCHAR(64) PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def login_user(email, password):
    """Login user"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", 
                   (email, hash_pw(password)))
        user = cur.fetchone()
        
        if user:
            # Create session token
            token = secrets.token_urlsafe(32)
            cur.execute("INSERT INTO user_sessions (token, user_id) VALUES (?, ?)", 
                       (token, user['id']))
            conn.commit()
            conn.close()
            return True, token, dict(user)
        
        conn.close()
        return False, None, None
        
    except Exception as e:
        print(f"Login error: {e}")
        return False, None, None

def register_user(fname, lname, email, password, phone=''):
    """Register new user"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cur.fetchone():
            conn.close()
            return False, "Email already registered"
        
        # Insert user
        cur.execute("""
            INSERT INTO users (fname, lname, email, password, phone)
            VALUES (?, ?, ?, ?, ?)
        """, (fname, lname, email, hash_pw(password), phone))
        
        conn.commit()
        conn.close()
        return True, "Registration successful"
        
    except Exception as e:
        print(f"Registration error: {e}")
        return False, f"Registration failed: {str(e)}"

def get_user_from_token(token):
    """Get user from session token"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT u.* FROM users u
            JOIN user_sessions s ON u.id = s.user_id
            WHERE s.token = ?
        """, (token,))
        
        user = cur.fetchone()
        conn.close()
        
        return dict(user) if user else None
        
    except Exception as e:
        print(f"Token validation error: {e}")
        return None

def logout_user(token):
    """Logout user"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM user_sessions WHERE token = ?", (token,))
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Logout error: {e}")
        return False

def email_already_registered(email):
    """Check if email is already registered"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()
        
        return user is not None
        
    except Exception as e:
        print(f"Email check error: {e}")
        return False

def store_pending_user(fname, lname, email, password):
    """Store pending user for email verification"""
    import secrets
    code = ''.join(str(secrets.randbelow(10)) for _ in range(6))
    
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO pending_users (fname, lname, email, password, code)
            VALUES (?, ?, ?, ?, ?)
        """, (fname, lname, email, hash_pw(password), code))
        
        conn.commit()
        conn.close()
        
        return code
        
    except Exception as e:
        print(f"Store pending user error: {e}")
        return None

def activate_user(email, code):
    """Activate user account from email verification"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Find pending user
        cur.execute("""
            SELECT fname, lname, email, password FROM pending_users
            WHERE email = ? AND code = ?
        """, (email, code))
        
        pending = cur.fetchone()
        if not pending:
            conn.close()
            return False, "Invalid verification code"
        
        # Move to users table
        cur.execute("""
            INSERT INTO users (fname, lname, email, password)
            VALUES (?, ?, ?, ?)
        """, (pending['fname'], pending['lname'], pending['email'], pending['password']))
        
        # Remove from pending
        cur.execute("DELETE FROM pending_users WHERE email = ?", (email,))
        
        conn.commit()
        conn.close()
        
        return True, "Account activated successfully"
        
    except Exception as e:
        print(f"Activate user error: {e}")
        return False, f"Activation failed: {str(e)}"

# Initialize tables on import
init_user_tables()
