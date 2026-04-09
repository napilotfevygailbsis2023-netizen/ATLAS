# ─────────────────────────────────────────────────────────────
#  ADD THIS FUNCTION TO YOUR EXISTING db.py FILE
#  Paste it at the bottom, before any if __name__ == "__main__"
# ─────────────────────────────────────────────────────────────

def login_or_create_google_user(email: str, fname: str, lname: str, photo_url: str = "") -> str | None:
    """
    Find an existing user by email (or google_id) and return a session token.
    If no user exists, auto-register them with no password (Google-only account).
    Returns a session token string on success, or None on failure.
    """
    conn = None
    try:
        conn = get_conn()          # use whatever your db.py calls to get a connection
        cur  = conn.cursor(dictionary=True)

        # 1. Try to find by email
        cur.execute("SELECT * FROM users WHERE email = %s LIMIT 1", (email,))
        user = cur.fetchone()

        if user:
            user_id = user["id"]
            # Update photo_url if Google provided one and we don't have one yet
            if photo_url and not user.get("photo_url"):
                cur.execute("UPDATE users SET photo_url=%s WHERE id=%s", (photo_url, user_id))
                conn.commit()
        else:
            # 2. Auto-register new Google user (no password)
            cur.execute(
                """INSERT INTO users (fname, lname, email, password, photo_url, is_verified)
                   VALUES (%s, %s, %s, NULL, %s, 1)""",
                (fname, lname, email, photo_url)
            )
            conn.commit()
            user_id = cur.lastrowid

        # 3. Create a session token
        import secrets, datetime
        token   = secrets.token_hex(32)
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        cur.execute(
            "INSERT INTO sessions (user_id, token, expires_at) VALUES (%s, %s, %s)",
            (user_id, token, expires)
        )
        conn.commit()
        cur.close()
        return token

    except Exception as e:
        print(f"[DB] login_or_create_google_user error: {e}")
        return None
    finally:
        if conn:
            try: conn.close()
            except: pass
