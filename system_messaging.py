import sys, os, datetime, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

def init_messaging_tables():
    """Initialize system messaging tables"""
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS system_threads (
                id VARCHAR(36) PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                created_by INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'active',
                thread_type VARCHAR(50) DEFAULT 'general'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS system_messages (
                id VARCHAR(36) PRIMARY KEY,
                thread_id VARCHAR(36) NOT NULL,
                sender_id INT NOT NULL,
                message_text TEXT NOT NULL,
                message_type VARCHAR(50) DEFAULT 'text',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                is_read BOOLEAN DEFAULT FALSE,
                metadata JSON
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS thread_participants (
                id VARCHAR(36) PRIMARY KEY,
                thread_id VARCHAR(36) NOT NULL,
                user_id INT NOT NULL,
                role VARCHAR(50) DEFAULT 'participant',
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_read_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS collective_memory (
                id VARCHAR(36) PRIMARY KEY,
                key_name VARCHAR(100) NOT NULL,
                value TEXT NOT NULL,
                category VARCHAR(50) DEFAULT 'general',
                created_by INT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                is_public BOOLEAN DEFAULT TRUE,
                tags JSON
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error initializing messaging tables: {e}")
        return False

def create_thread(title, created_by, thread_type='general', participants=None):
    """Create a new system thread"""
    try:
        import uuid
        thread_id = str(uuid.uuid4())
        
        conn = db.get_conn()
        cur = conn.cursor()
        
        # Create thread
        cur.execute("""
            INSERT INTO system_threads (id, title, created_by, thread_type)
            VALUES (%s, %s, %s, %s)
        """, (thread_id, title, created_by, thread_type))
        
        # Add creator as participant
        cur.execute("""
            INSERT INTO thread_participants (id, thread_id, user_id, role)
            VALUES (%s, %s, %s, %s)
        """, (str(uuid.uuid4()), thread_id, created_by, 'creator'))
        
        # Add additional participants if provided
        if participants:
            for participant_id in participants:
                cur.execute("""
                    INSERT INTO thread_participants (id, thread_id, user_id, role)
                    VALUES (%s, %s, %s, %s)
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
        import uuid
        message_id = str(uuid.uuid4())
        
        conn = db.get_conn()
        cur = conn.cursor()
        
        # Verify sender is a participant
        cur.execute("""
            SELECT COUNT(*) FROM thread_participants 
            WHERE thread_id = %s AND user_id = %s AND is_active = TRUE
        """, (thread_id, sender_id))
        
        if cur.fetchone()[0] == 0:
            conn.close()
            return False, "User is not a participant in this thread"
        
        # Add message
        cur.execute("""
            INSERT INTO system_messages (id, thread_id, sender_id, message_text, message_type, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (message_id, thread_id, sender_id, message_text, message_type, 
              json.dumps(metadata) if metadata else None))
        
        # Update thread timestamp
        cur.execute("""
            UPDATE system_threads 
            SET updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
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
        conn = db.get_conn()
        cur = conn.cursor(dictionary=True)
        
        # Verify user is a participant
        cur.execute("""
            SELECT COUNT(*) FROM thread_participants 
            WHERE thread_id = %s AND user_id = %s AND is_active = TRUE
        """, (thread_id, user_id))
        
        if cur.fetchone()[0] == 0:
            conn.close()
            return []
        
        # Get messages
        cur.execute("""
            SELECT m.*, u.fname, u.lname, u.email
            FROM system_messages m
            JOIN users u ON m.sender_id = u.id
            WHERE m.thread_id = %s
            ORDER BY m.created_at ASC
            LIMIT %s
        """, (thread_id, limit))
        
        messages = cur.fetchall()
        
        # Mark messages as read
        cur.execute("""
            UPDATE system_messages 
            SET is_read = TRUE 
            WHERE thread_id = %s AND sender_id != %s AND is_read = FALSE
        """, (thread_id, user_id))
        
        # Update participant's last read time
        cur.execute("""
            UPDATE thread_participants 
            SET last_read_at = CURRENT_TIMESTAMP 
            WHERE thread_id = %s AND user_id = %s
        """, (thread_id, user_id))
        
        conn.commit()
        conn.close()
        return messages
        
    except Exception as e:
        print(f"Error getting thread messages: {e}")
        return []

def get_user_threads(user_id):
    """Get all threads for a user"""
    try:
        conn = db.get_conn()
        cur = conn.cursor(dictionary=True)
        
        cur.execute("""
            SELECT t.*, 
                   (SELECT COUNT(*) FROM system_messages m 
                    WHERE m.thread_id = t.id AND m.is_read = FALSE AND m.sender_id != %s) as unread_count,
                   (SELECT m.message_text FROM system_messages m 
                    WHERE m.thread_id = t.id 
                    ORDER BY m.created_at DESC LIMIT 1) as last_message,
                   (SELECT m.created_at FROM system_messages m 
                    WHERE m.thread_id = t.id 
                    ORDER BY m.created_at DESC LIMIT 1) as last_message_time
            FROM system_threads t
            JOIN thread_participants p ON t.id = p.thread_id
            WHERE p.user_id = %s AND p.is_active = TRUE
            ORDER BY t.updated_at DESC
        """, (user_id, user_id))
        
        threads = cur.fetchall()
        conn.close()
        return threads
        
    except Exception as e:
        print(f"Error getting user threads: {e}")
        return []

def store_collective_memory(key_name, value, category='general', created_by=None, is_public=True, tags=None):
    """Store information in collective memory"""
    try:
        import uuid
        memory_id = str(uuid.uuid4())
        
        conn = db.get_conn()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO collective_memory (id, key_name, value, category, created_by, is_public, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            value = VALUES(value), 
            updated_at = CURRENT_TIMESTAMP,
            tags = VALUES(tags)
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
        conn = db.get_conn()
        cur = conn.cursor(dictionary=True)
        
        if category:
            cur.execute("""
                SELECT * FROM collective_memory 
                WHERE key_name = %s AND category = %s AND is_public = TRUE
            """, (key_name, category))
        else:
            cur.execute("""
                SELECT * FROM collective_memory 
                WHERE key_name = %s AND is_public = TRUE
            """, (key_name,))
        
        memory = cur.fetchone()
        conn.close()
        return memory
        
    except Exception as e:
        print(f"Error retrieving collective memory: {e}")
        return None

def search_collective_memory(query, category=None, limit=20):
    """Search collective memory"""
    try:
        conn = db.get_conn()
        cur = conn.cursor(dictionary=True)
        
        if category:
            cur.execute("""
                SELECT * FROM collective_memory 
                WHERE (key_name LIKE %s OR value LIKE %s) 
                AND category = %s AND is_public = TRUE
                ORDER BY updated_at DESC
                LIMIT %s
            """, (f'%{query}%', f'%{query}%', category, limit))
        else:
            cur.execute("""
                SELECT * FROM collective_memory 
                WHERE (key_name LIKE %s OR value LIKE %s) 
                AND is_public = TRUE
                ORDER BY updated_at DESC
                LIMIT %s
            """, (f'%{query}%', f'%{query}%', limit))
        
        memories = cur.fetchall()
        conn.close()
        return memories
        
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

def render_thread_list(user_id):
    """Render thread list for user"""
    threads = get_user_threads(user_id)
    
    if not threads:
        return '<div style="text-align:center;padding:40px;color:#6B7280">No threads found. Start a conversation!</div>'
    
    thread_html = ""
    for thread in threads:
        unread_badge = f'<span style="background:#DC2626;color:#fff;padding:2px 6px;border-radius:10px;font-size:10px;font-weight:700">{thread["unread_count"]}</span>' if thread.get('unread_count', 0) > 0 else ''
        
        last_msg_preview = thread.get('last_message', '')[:50] + '...' if len(thread.get('last_message', '')) > 50 else thread.get('last_message', 'No messages yet')
        
        thread_html += f"""
        <div class="thread-item" style="border:1px solid #E5E7EB;border-radius:8px;padding:12px;margin-bottom:8px;cursor:pointer" onclick="openThread('{thread['id']}')">
            <div style="display:flex;justify-content:space-between;align-items:start">
                <div style="flex:1">
                    <div style="font-weight:700;color:#1F2937;margin-bottom:4px">{thread['title']} {unread_badge}</div>
                    <div style="font-size:13px;color:#6B7280">{last_msg_preview}</div>
                </div>
                <div style="font-size:11px;color:#9CA3AF;text-align:right">
                    {thread.get('last_message_time', '').strftime('%H:%M') if thread.get('last_message_time') else ''}
                </div>
            </div>
        </div>"""
    
    return thread_html

def render_system_status():
    """Render system status updates"""
    status_updates = get_system_status_updates()
    
    if not status_updates:
        return '<div style="text-align:center;padding:20px;color:#6B7280">No system updates available.</div>'
    
    status_html = ""
    for status in status_updates:
        priority_colors = {
            'high': ('#DC2626', '#FEF2F2'),
            'normal': ('#0038A8', '#EFF6FF'),
            'low': ('#059669', '#ECFDF5')
        }
        
        tags = json.loads(status.get('tags', '[]')) if status.get('tags') else []
        priority = 'normal'
        for tag in tags:
            if tag in priority_colors:
                priority = tag
                break
        
        color, bg = priority_colors.get(priority, priority_colors['normal'])
        
        status_html += f"""
        <div style="background:{bg};border-left:3px solid {color};padding:12px;border-radius:6px;margin-bottom:8px">
            <div style="font-weight:700;color:{color};margin-bottom:4px">System Update</div>
            <div style="font-size:13px;color:#374151">{status['value']}</div>
            <div style="font-size:11px;color:#9CA3AF;margin-top:4px">{status['updated_at'].strftime('%Y-%m-%d %H:%M')}</div>
        </div>"""
    
    return status_html
