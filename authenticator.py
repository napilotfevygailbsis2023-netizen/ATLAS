import pyotp
import qrcode
import io
import base64
import secrets
import hashlib
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db_sqlite as db

def generate_secret():
    """Generate a new TOTP secret for a user"""
    return pyotp.random_base32()

def generate_qr_code(email, secret):
    """Generate QR code for Google Authenticator setup"""
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=email,
        issuer_name="ATLAS Travel"
    )
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def verify_totp(secret, token):
    """Verify TOTP token from Google Authenticator"""
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)

def enable_2fa_for_user(user_id, secret):
    """Enable 2FA for a user in database"""
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET totp_secret = %s, totp_enabled = 1 WHERE id = %s",
            (secret, user_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error enabling 2FA: {e}")
        return False

def disable_2fa_for_user(user_id):
    """Disable 2FA for a user in database"""
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET totp_secret = NULL, totp_enabled = 0 WHERE id = %s",
            (user_id,)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error disabling 2FA: {e}")
        return False

def get_user_2fa_status(user_id):
    """Get 2FA status for a user"""
    try:
        conn = db.get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT totp_enabled, totp_secret FROM users WHERE id = %s",
            (user_id,)
        )
        result = cur.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"Error getting 2FA status: {e}")
        return None

def verify_user_2fa(user_id, token):
    """Verify 2FA token for a user"""
    user_2fa = get_user_2fa_status(user_id)
    if not user_2fa or not user_2fa['totp_enabled'] or not user_2fa['totp_secret']:
        return False
    
    return verify_totp(user_2fa['totp_secret'], token)

def setup_2fa_database():
    """Add 2FA columns to users table if they don't exist"""
    try:
        conn = db.get_conn()
        cur = conn.cursor()
        
        # Add totp_secret column
        try:
            cur.execute("ALTER TABLE users ADD COLUMN totp_secret VARCHAR(32)")
        except:
            pass  # Column already exists
        
        # Add totp_enabled column
        try:
            cur.execute("ALTER TABLE users ADD COLUMN totp_enabled BOOLEAN DEFAULT 0")
        except:
            pass  # Column already exists
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error setting up 2FA database: {e}")
        return False
