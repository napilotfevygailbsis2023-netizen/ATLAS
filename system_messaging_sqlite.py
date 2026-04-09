import sqlite3
import uuid
import datetime
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'atlas.db')

def get_conn():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_messaging_tables():
    """Initialize system messaging tables"""
    conn = get_conn()
    cur = conn.cursor()
    
    # System threads table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS system_threads (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_by INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active',
            thread_type TEXT DEFAULT 'general'
        )
    """)
    
    # System messages table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS system_messages (
            id TEXT PRIMARY KEY,
            thread_id TEXT NOT NULL,
            sender_id INTEGER NOT NULL,
            message_text TEXT NOT NULL,
            message_type TEXT DEFAULT 'text',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_read BOOLEAN DEFAULT FALSE,
            metadata TEXT
        )
    """)
    
    # Thread participants table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS thread_participants (
            id TEXT PRIMARY KEY,
            thread_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            role TEXT DEFAULT 'participant',
            joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_read_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Collective memory table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS collective_memory (
            id TEXT PRIMARY KEY,
            key_name TEXT NOT NULL,
            value TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            created_by INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_public BOOLEAN DEFAULT TRUE,
            tags TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def create_thread(title, created_by, thread_type='general', participants=None):
    """Create a new system thread"""
    try:
        thread_id = str(uuid.uuid4())
        
        conn = get_conn()
        cur = conn.cursor()
        
        # Create thread
        cur.execute("""
            INSERT INTO system_threads (id, title, created_by, thread_type)
            VALUES (?, ?, ?, ?)
        """, (thread_id, title, created_by, thread_type))
        
        # Add creator as participant
        cur.execute("""
            INSERT INTO thread_participants (id, thread_id, user_id, role)
            VALUES (?, ?, ?, ?)
        """, (str(uuid.uuid4()), thread_id, created_by, 'creator'))
        
        # Add additional participants if provided
        if participants:
            for participant_id in participants:
                cur.execute("""
                    INSERT INTO thread_participants (id, thread_id, user_id, role)
                    VALUES (?, ?, ?, ?)
                """, (str(uuid.uuid4()), thread_id, participant_id, 'participant'))
        
        conn.commit()
        conn.close()
        return thread_id
        
    except Exception as e:
        print(f"Error creating thread: {e}")
        return None

def send_message(thread_id, sender_id, message_text, message_type='text', metadata=None):
    """Send a message to a thread"""
    try:
        message_id = str(uuid.uuid4())
        
        conn = get_conn()
        cur = conn.cursor()
        
        # Verify sender is a participant
        cur.execute("""
            SELECT COUNT(*) FROM thread_participants 
            WHERE thread_id = ? AND user_id = ? AND is_active = 1
        """, (thread_id, sender_id))
        
        if cur.fetchone()[0] == 0:
            conn.close()
            return False, "User is not a participant in this thread"
        
        # Add message
        cur.execute("""
            INSERT INTO system_messages (id, thread_id, sender_id, message_text, message_type, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (message_id, thread_id, sender_id, message_text, message_type, 
              json.dumps(metadata) if metadata else None))
        
        # Update thread timestamp
        cur.execute("""
            UPDATE system_threads 
            SET updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (thread_id,))
        
        conn.commit()
        conn.close()
        return message_id, "Message sent successfully"
        
    except Exception as e:
        print(f"Error sending message: {e}")
        return None, f"Error sending message: {str(e)}"

def get_thread_messages(thread_id, user_id, limit=50):
    """Get messages from a thread"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        # Verify user is a participant
        cur.execute("""
            SELECT COUNT(*) FROM thread_participants 
            WHERE thread_id = ? AND user_id = ? AND is_active = 1
        """, (thread_id, user_id))
        
        if cur.fetchone()[0] == 0:
            conn.close()
            return []
        
        # Get messages
        cur.execute("""
            SELECT m.*, u.fname, u.lname, u.email
            FROM system_messages m
            LEFT JOIN users u ON m.sender_id = u.id
            WHERE m.thread_id = ?
            ORDER BY m.created_at ASC
            LIMIT ?
        """, (thread_id, limit))
        
        messages = cur.fetchall()
        
        # Mark messages as read
        cur.execute("""
            UPDATE system_messages 
            SET is_read = 1 
            WHERE thread_id = ? AND sender_id != ? AND is_read = 0
        """, (thread_id, user_id))
        
        # Update participant's last read time
        cur.execute("""
            UPDATE thread_participants 
            SET last_read_at = CURRENT_TIMESTAMP 
            WHERE thread_id = ? AND user_id = ?
        """, (thread_id, user_id))
        
        conn.commit()
        conn.close()
        return [dict(row) for row in messages]
        
    except Exception as e:
        print(f"Error getting thread messages: {e}")
        return []

def get_user_threads(user_id):
    """Get all threads for a user"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT t.*, 
                   (SELECT COUNT(*) FROM system_messages m 
                    WHERE m.thread_id = t.id AND m.is_read = 0 AND m.sender_id != ?) as unread_count,
                   (SELECT m.message_text FROM system_messages m 
                    WHERE m.thread_id = t.id 
                    ORDER BY m.created_at DESC LIMIT 1) as last_message,
                   (SELECT m.created_at FROM system_messages m 
                    WHERE m.thread_id = t.id 
                    ORDER BY m.created_at DESC LIMIT 1) as last_message_time
            FROM system_threads t
            JOIN thread_participants p ON t.id = p.thread_id
            WHERE p.user_id = ? AND p.is_active = 1
            ORDER BY t.updated_at DESC
        """, (user_id, user_id))
        
        threads = cur.fetchall()
        conn.close()
        return [dict(row) for row in threads]
        
    except Exception as e:
        print(f"Error getting user threads: {e}")
        return []

def store_collective_memory(key_name, value, category='general', created_by=None, is_public=True, tags=None):
    """Store information in collective memory"""
    try:
        memory_id = str(uuid.uuid4())
        
        conn = get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT OR REPLACE INTO collective_memory (id, key_name, value, category, created_by, is_public, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (memory_id, key_name, value, category, created_by, is_public, 
              json.dumps(tags) if tags else None))
        
        conn.commit()
        conn.close()
        return memory_id
        
    except Exception as e:
        print(f"Error storing collective memory: {e}")
        return None

def retrieve_collective_memory(key_name, category=None):
    """Retrieve information from collective memory"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        if category:
            cur.execute("""
                SELECT * FROM collective_memory 
                WHERE key_name = ? AND category = ? AND is_public = 1
            """, (key_name, category))
        else:
            cur.execute("""
                SELECT * FROM collective_memory 
                WHERE key_name = ? AND is_public = 1
            """, (key_name,))
        
        memory = cur.fetchone()
        conn.close()
        return dict(memory) if memory else None
        
    except Exception as e:
        print(f"Error retrieving collective memory: {e}")
        return None

def search_collective_memory(query, category=None, limit=20):
    """Search collective memory"""
    try:
        conn = get_conn()
        cur = conn.cursor()
        
        if category:
            cur.execute("""
                SELECT * FROM collective_memory 
                WHERE (key_name LIKE ? OR value LIKE ?) 
                AND category = ? AND is_public = 1
                ORDER BY updated_at DESC
                LIMIT ?
            """, (f'%{query}%', f'%{query}%', category, limit))
        else:
            cur.execute("""
                SELECT * FROM collective_memory 
                WHERE (key_name LIKE ? OR value LIKE ?) 
                AND is_public = 1
                ORDER BY updated_at DESC
                LIMIT ?
            """, (f'%{query}%', f'%{query}%', limit))
        
        memories = cur.fetchall()
        conn.close()
        return [dict(row) for row in memories]
        
    except Exception as e:
        print(f"Error searching collective memory: {e}")
        return []

def get_system_status_updates():
    """Get system status updates from collective memory"""
    try:
        memories = search_collective_memory('status', category='system', limit=10)
        return memories
    except Exception as e:
        print(f"Error getting system status updates: {e}")
        return []

def add_status_update(status_message, created_by, priority='normal'):
    """Add a system status update"""
    tags = ['status', 'system', priority]
    return store_collective_memory(
        f"status_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
        status_message,
        category='system',
        created_by=created_by,
        is_public=True,
        tags=tags
    )

# Initialize tables on import
init_messaging_tables()
