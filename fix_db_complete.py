#!/usr/bin/env python3
"""
Complete database fix for SQLite
"""

import os
import sqlite3

def fix_database():
    """Fix all database issues"""
    
    # Remove old database file to start fresh
    db_path = os.path.join(os.path.dirname(__file__), 'atlas.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed old database file")
    
    # Create fresh database with correct schema
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Users table
    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname VARCHAR(100) NOT NULL,
            lname VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            phone VARCHAR(50) DEFAULT '',
            photo_url VARCHAR(500) DEFAULT '',
            totp_secret VARCHAR(32),
            totp_enabled BOOLEAN DEFAULT 0,
            status VARCHAR(20) DEFAULT 'active',
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Sessions table
    cur.execute("""
        CREATE TABLE sessions (
            token VARCHAR(64) PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Admins table
    cur.execute("""
        CREATE TABLE admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Admin sessions table
    cur.execute("""
        CREATE TABLE admin_sessions (
            token VARCHAR(64) PRIMARY KEY,
            admin_id INTEGER NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tour guides table
    cur.execute("""
        CREATE TABLE tour_guides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname VARCHAR(100) NOT NULL,
            lname VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(64) NOT NULL,
            phone VARCHAR(50) DEFAULT '',
            city VARCHAR(100) NOT NULL,
            languages TEXT,
            specialties TEXT,
            bio TEXT,
            photo_url VARCHAR(500) DEFAULT '',
            rating FLOAT DEFAULT 0.0,
            status VARCHAR(20) DEFAULT 'active',
            permit_number VARCHAR(100),
            permit_expiry DATE,
            license_number VARCHAR(100),
            license_expiry DATE,
            verification_status VARCHAR(20) DEFAULT 'pending',
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Guide sessions table
    cur.execute("""
        CREATE TABLE guide_sessions (
            token VARCHAR(64) PRIMARY KEY,
            guide_id INTEGER NOT NULL,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tour packages table
    cur.execute("""
        CREATE TABLE tour_packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guide_id INTEGER NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            duration VARCHAR(100),
            price VARCHAR(100),
            max_group_size INTEGER DEFAULT 10,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Bookings table
    cur.execute("""
        CREATE TABLE bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guide_id INTEGER NOT NULL,
            tourist_name VARCHAR(200) NOT NULL,
            tourist_email VARCHAR(255) NOT NULL,
            tourist_phone VARCHAR(50),
            package_title VARCHAR(200),
            tour_date DATE,
            pax INTEGER DEFAULT 1,
            status VARCHAR(20) DEFAULT 'pending',
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Guide ratings table
    cur.execute("""
        CREATE TABLE guide_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guide_id INTEGER NOT NULL,
            booking_id INTEGER,
            rating INTEGER NOT NULL,
            comment TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Flight bookings table
    cur.execute("""
        CREATE TABLE flight_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_reference VARCHAR(20) UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            flight_number VARCHAR(20) NOT NULL,
            origin VARCHAR(100) NOT NULL,
            destination VARCHAR(100) NOT NULL,
            departure_datetime DATETIME NOT NULL,
            arrival_datetime DATETIME NOT NULL,
            passenger_name VARCHAR(200) NOT NULL,
            passenger_email VARCHAR(255) NOT NULL,
            status VARCHAR(20) DEFAULT 'confirmed',
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # System threads table
    cur.execute("""
        CREATE TABLE system_threads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            created_by INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    """)
    
    # System messages table
    cur.execute("""
        CREATE TABLE system_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id INTEGER NOT NULL,
            sender_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Collective memory table
    cur.execute("""
        CREATE TABLE collective_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            category VARCHAR(100),
            tags TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert default admin
    import hashlib
    admin_password = hashlib.sha256("atlas2026".encode()).hexdigest()
    cur.execute("INSERT INTO admins (username, password, email) VALUES (?, ?, ?)", 
               ("admin", admin_password, "admin@atlas.com"))
    
    conn.commit()
    conn.close()
    
    print("Database fixed successfully!")
    return True

if __name__ == "__main__":
    fix_database()
